import streamlit as st
import os
import pandas as pd
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.query import MetadataQuery
import json

# Load environment variables (useful when working locally)
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Simple Vector Database Search",
    page_icon="🧊",
    layout="wide",
)

st.title('Simple Vector Database Search')

st.markdown('Search a Weaviate Cloud database for matches to a query (it can take a few seconds to return a result).')

collectionname = os.environ['collectionname']

# Perform the process here
try:
    print(f"Using collection name {collectionname}")

    with weaviate.connect_to_wcs(
            cluster_url=os.environ["weaviate_rest_endpoint"],
            auth_credentials=AuthApiKey(os.environ["weaviate_apikey"]),
            headers={'X-OpenAI-Api-key': os.getenv("OPENAI_API_KEY")}
            ) as client:
                # Do something with the client
                mycollection = client.collections.get(collectionname)

                # Create a text input field for the search term
                col, buff = st.columns([4, 5])
                search_term = col.text_input("Enter your search term")
                search_result = []

                count = mycollection.aggregate.over_all(total_count=True)
                total_count = count.total_count

                if total_count == 0:
                    st.write("Collection is empty")
                else:
                    st.write(f"Collection contains {total_count} entries.")

                if search_term != "":

                    try:
                        # Use Weaviate's built-in OpenAI integration to vectorize the search term
                        response = mycollection.query.near_text(
                            query=search_term,
                            limit=5,
                            return_metadata=MetadataQuery(distance=True))
                        # Initialize a list to hold each row of data
                        resultdata = []

                        # Iterate through the search results
                        for o in response.objects:
                                resultdata.append(o.properties)

                        df = pd.DataFrame(resultdata)

                        # Display the results in a Streamlit app
                        st.markdown('**Weaviate Search Results**')

                        if len(resultdata) < 1:
                            print("No matches")
                        else:
                            st.write(df)

                    except Exception as e:
                        print(f"Exception: {e}")


except Exception as e:
    print(f"Exception: {e}")