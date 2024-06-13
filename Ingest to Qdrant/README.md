# Ingesting vectors into Qdrant using Quix Streams

## Overview
This Python application integrates Quix Streams with a local Qdrant Vector Database to ingest vector data efficiently. It is tailored for handling real-time data streams, specifically ingesting vector embeddings and related metadata into a vector database.

## Functionality
- **Data Input**: Reads vectors and metadata from an input topic using environment variables for the topic name.
- **Data Processing**:
  - Ingests vectors and metadata (like name, description, author, year) into a Qdrant Vector Database.

## Configuration
Set environment variables for the input topic and Upstash Vector Database credentials (endpoint and token) before running the script.

## Dependencies
- quixstreams
- qdrant-client

## Usage
Ensure that the Quix Streams and Qdrant dependencies are set up in your environment. Run the application after setting the required environment variables for it to automatically ingest data to the configured vector database.

