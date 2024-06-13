import streamlit as st
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
import os
import pandas as pd

# This will trigger the model download and initialization
embedding_model = TextEmbedding()
print("The model BAAI/bge-small-en-v1.5 is ready to use.")

collectionname = os.environ['qd_collection']

st.title('Simple Vector Database Search')

st.markdown('Search a Qdrant Cloud database for matches to a query (it can take a few seconds to return a result).')

# Perform the process here
try:
    print(f"Using collection name {collectionname}")

    # Initialize the QdrantClient
    qdrant = QdrantClient(host=os.environ['qd_host'], port=os.environ['qd_port'])

    # Get the collection to search
    qdrant.get_collection(collection_name=collectionname)

except Exception as e:
    qdrant = "Error"
    print(f"Exception: {e}")

# Create a text input field for the search term
search_term = st.text_input("Enter your search term")
search_result = []

if search_term != "":

    try:
        # Vectorize the search term
        embeddings = list(embedding_model.embed([search_term]))
        embedding_list = [embedding.tolist() for embedding in embeddings]
        query_vector = embedding_list[0]

        total_points = qdrant.get_collection(collection_name=collectionname).points_count
        if total_points == 0:
            st.write("Collection is empty")
        else:
            # Query the database
            search_result = qdrant.search(
                collection_name=collectionname,
                query_vector=query_vector,
                limit=5
            )

            # Initialize a list to hold each row of data
            resultdata = []

            # Iterate through the search results
            for result in search_result:
                # Extracting data from each result
                row = {
                    'name': result.payload['name'],
                    'description': result.payload['description'],
                    'score': result.score,
                    'author': result.payload['author'],
                    'year': str(result.payload['year']),
                    'id': result.id,
                }
                resultdata.append(row)
            df = pd.DataFrame(resultdata)

            print(f"Total points stored {total_points}")
            # Display the results in a Streamlit app
            st.markdown('**Qdrant Search Results**')

            if len(search_result) < 1:
                print("No matches")
            else:
                st.write(df)

    except Exception as e:
        print(f"Exception: {e}")