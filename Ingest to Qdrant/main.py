from quixstreams import Application
from qdrant_client import models, QdrantClient
import os

from dotenv import load_dotenv
load_dotenv()

host = os.getenv("qd_host", "")
port = os.getenv("qd_port", "")
collection = os.getenv("qd_collection", "")

qdrant = QdrantClient(host=host, port=port)
collection = collection

# Create collection to store items
if not qdrant.collection_exists(collection):
    # Define the collection parameters
    vector_size = 384
    # Create the collection
    qdrant.create_collection(
        collection_name=collection,
        vectors_config=models.VectorParams(
            size=vector_size,  # Vector size is defined by used model
            distance=models.Distance.COSINE
        )
    )
    print(f"Collection '{collection}' created.")
else:
    print(f"Collection '{collection}' already exists.")

# Define the ingestion function
def ingest_vectors(row):

  single_record = models.PointStruct(
    id=row['id'],
    vector=row['embeddings'],
    payload={key: row[key] for key in ['name', 'description', 'author', 'year']}
    )

  qdrant.upload_points(
      collection_name=collection,
      points=[single_record]
    )

  print(f'Ingested vector entry id: "{row["id"]}"...')

app = Application(
    consumer_group="ingesterV1",
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json") # Merlin.. i updated this for you

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

# INGESTION HAPPENS HERE
sdf = sdf.update(lambda row: ingest_vectors(row))
app.run(sdf)