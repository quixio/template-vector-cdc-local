# Using the Streamlit Vector Search UI
The demo application contains a simple search UI (built with Streamlit) to help you test the vector search. 

You can access it under the URL: _http://localhost:8082_

For example, in the search UI, try searching for "battle in space" - the top result should be "The War of the Worlds". It's not quite right since the book is about a battle that takes place on Earth, but it looks like it's currently the best batch in our book catalog.

![Streamlit Screenshot](https://github.com/quixio/template-vector-cdc-local/assets/116729413/71ee419c-c8cc-44e3-bfa9-d761ccd827dc)

_We can speculate that it matched as the top result because "Martian" is semantically close to "space" and "invasion" is semantically close to "battle". Note that you'll likely get a different result if you use a more sophisticated embedding model such as sentence transformers, however, it's a pretty heavy library which is why we left it out of this demo._
