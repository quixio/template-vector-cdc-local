# Application to Create Embeddings 

## Overview
This Python application uses Quix Streams to process real-time data and creates embeddings for a text field called "description" using the Sentence Transformer library. It is designed to process a Change Data Capture (CDC) data stream for updates to a book catalog, creating embeddings for the book descriptions, and publishing the results to an output topic.

## Functionality
- **Data Input/Output**: Reads data from an input topic and writes to an output topic using environment variables for topic names.
- **Data Processing**:
  - Filters rows specific to books.
  - Simplifies data structure by merging and converting fields.
  - Generates text embeddings for descriptions using `all-MiniLM-L6-v2` model.

## Configuration
Set environment variables for input and output topics before running the script.

## Dependencies
- quixstreams
- sentence-transformers

## Usage
Execute the script in an environment where Quix Streams and the required Python packages are available. The script is configured to auto-create topics and begin processing as soon as it is launched.

