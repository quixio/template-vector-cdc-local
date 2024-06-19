import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.query import MetadataQuery
import os

# Load environment variables (useful when working locally)
from dotenv import load_dotenv
load_dotenv()

client = weaviate.connect_to_wcs(
        cluster_url=os.environ["weaviate_rest_endpoint"],
        auth_credentials=AuthApiKey(os.environ["weaviate_apikey"]),
        headers={'X-OpenAI-Api-key': os.getenv("OPENAI_API_KEY")}
)

mycollection = client.collections.get("Products")
response = mycollection.query.near_text(
    query="shoes",
    limit=2,
    return_metadata=MetadataQuery(distance=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.distance)

client.close()