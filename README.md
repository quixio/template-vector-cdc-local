# Local Change Data Capture (CDC) Tutorial: PostgreSQL to a vector DB via Redpanda

## Overview
This repository accompanies the blog article "Synchronize a PostgreSQL DB with a Vector DB using Python and CDC". It demonstrates how to efficiently capture data changes in a PostgreSQL database and stream them into a local vector database (Qdrant) using Redpanda (Kafka-like message broker), Python, and the Quix Streams Python library.

## Why Change Data Capture?
Change Data Capture (CDC) is crucial for RAG-powered applications that require real-time data accuracy, such as AI-chatbots in e-commerce. By only processing and transmitting changed data, CDC minimizes data latency and reduces resource consumption.

## Architecture
![CDC Pipeline Screenshot](https://github.com/quixio/template-vector-cdc-local/assets/116729413/f2c236ab-3455-4d8a-b8bb-e006849215d8)

This tutorial leverages:
- **PostgreSQL**: Source database for capturing changes.
- **Redpanda**: A Kafka-compatible streaming data platform that is easy to run locally.
- **Quix Streams**: A Python-based framework for stream processing, handling the ingestion and transformation of streaming data.
- **Qdrant**: An open-source vector database designed for efficient and scalable similarity search and nearest neighbor search tasks
- **Streamlit**: An open-source Python library that simplifies the process of creating and sharing custom web applications for machine learning and data science projects. 

## Getting Started
1. **Prerequisites**: Docker must be installed on your local machine.
3. **Run**: `docker compose up -d` to build and start the services.

## How It Works
1. **Capture Changes**: Detects and captures data modifications in PostgreSQL.
2. **Process Data**: Python scripts use the Quix Streams library to transform data into a suitable format for vector databases.
3. **Upsert Data**: Stream the transformed data into the Qdrant Vector DB for quick retrieval and querying.
4. **Query Data**: Test the similarity search in the prototype Streamlit search UI.

## Resources
- **Code**: Explore the full source code provided in this repository.
- **Documentation**: Detailed instructions are available in the accompanying blog article and the READMEs of individual components within this repo.


## Support
Join the Quix Community Slack for support and discussions about real-time data processing with Quix and Upstash.
