from quixstreams import Application
import weaviate
import weaviate.classes as wvc
import os
import logging
from urllib.parse import urlparse
import requests
import base64

# Load environment variables (useful when working locally)
from dotenv import load_dotenv
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"WEAVIATE URL {os.environ['weaviate_rest_endpoint']}")
targettable = os.environ['PG_TABLE']

# Initialize the Weaviate client. Replace the placeholder values with your actual Weaviate instance details.
wclient = weaviate.connect_to_wcs(
    cluster_url=os.environ["weaviate_rest_endpoint"],  # Replace with your WCS URL
    auth_credentials=weaviate.auth.AuthApiKey(os.environ["weaviate_apikey"]),  # Replace with your WCS key
    # OPENAI KEY ONLY NEEDED FOR GENERATIVE SEARCH
    headers={'X-OpenAI-Api-key': os.getenv("OPENAI_APIKEY")}  # Replace with your OpenAI API key
)

collectionname = os.environ["collectionname"]
if not wclient.collections.exists(collectionname):  # if the schema/collection is missing create it
    vectorizer_config = wvc.config.Configure.Vectorizer.text2vec_openai()
    generative_config = wvc.config.Configure.Generative.openai()

    mycollection = wclient.collections.create(
        name=collectionname,
        vectorizer_config=vectorizer_config,
        generative_config=generative_config,
        properties=[
            wvc.config.Property(
                name="product_id",
                data_type=wvc.config.DataType.TEXT,
                skip_vectorization=True,
                index_filterable=False,
                index_searchable=False
            ),
            wvc.config.Property(
                name="title",
                data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(
                name="category",
                data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(
                name="sub_category",
                data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(
                name="image_url",
                data_type=wvc.config.DataType.TEXT,
                skip_vectorization=True,
                index_filterable=False,
                index_searchable=False,
            ),
            wvc.config.Property(
                name="brand",
                data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(
                name="description",
                data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(
                name="color",
                data_type=wvc.config.DataType.TEXT_ARRAY
            ),
            wvc.config.Property(
                name="material",
                data_type=wvc.config.DataType.TEXT_ARRAY
            ),
            wvc.config.Property(
                name="price",
                data_type=wvc.config.DataType.NUMBER
            ),
            wvc.config.Property(
                name="rating",
                data_type=wvc.config.DataType.NUMBER
            )
        ],
    )

else:
    mycollection = wclient.collections.get(collectionname)  # if the collection already existed just refer to it

def simplify_data(row):

    # Creating a new dictionary that includes 'kind' and zips column names with values
    new_structure = {"kind": row["kind"],"table": row["table"]}
    new_structure.update({key: value for key, value in zip(row["columnnames"], row["columnvalues"])})

    return new_structure


# ADDITIONAL FUNCTION TO DOWNLOAD AND EMBED IMAGES
def download_image(row):
    url = row['imgurl']
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    file_path = os.path.join("state", filename)
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    # Save the image to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)

    b64string = base64.b64encode(response.content).decode('utf-8')

    return b64string

# Define the ingestion function
def ingest_vectors(row):

    try:
        row['color'] = row['color'].strip('{}').split(',')
        row['material'] = row['material'].strip('{}').split(',')
        uuid = mycollection.data.insert(
            properties={
                "product_id": row["product_id"],
                "title": row["title"],
                "category": row["category"],
                "description": row["description"],
                "sub_category": row["sub_category"],
                "image_url": row["image_url"],
                "brand": row["brand"],
                "color": row["color"],
                "material": row["material"],
                "price": float(row["price"]),
                "rating": float(row["rating"]),
                },
                uuid=row["product_id"]
            )

        print(f'Ingested vector entry id: "{uuid}"...')

    except Exception as e:
        print(f"Error because of: {e}")


app = Application(
    consumer_group=os.environ["groupname"],
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json")

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

sdf = sdf.filter(lambda data: data["table"] == targettable)

sdf = sdf.apply(simplify_data)
sdf = sdf.update(lambda val: logger.info(f"Simplified data: {val}"))
sdf["imgbs64"] = sdf.apply(download_image, stateful=False) # Add the image as a base64 string to the payload

# INGESTION HAPPENS HERE
sdf = sdf.update(lambda row: ingest_vectors(row))

if __name__ == "__main__":
    try:
        # Start message processing
        app.run(sdf)
    except KeyboardInterrupt:
        logger.info("Exiting.")
        run = False
    finally:
        wclient.close()
        logger.info("Connection to Weaviate closed")
        logger.info("Exiting")

