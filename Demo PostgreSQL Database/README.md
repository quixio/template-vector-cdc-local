# PostgreSQL Docker Setup with Logical Replication

## Overview
This Docker setup provides a PostgreSQL database server for testing with Quix CDC. It has the `wal2json` extension installed, facilitating logical replication. It's configured with default credentials and a test database, suitable for development environments.

## Features
- **PostgreSQL 13**: Utilizes a specific version for compatibility.
- **wal2json**: Extension built and installed for outputting changes in JSON format.
- **Logical Replication Enabled**: Configured with `wal_level=logical` to support logical decoding.
- **Pre-configured Database**: Includes a predefined user, password, and database.


## Configuration
The Dockerfile sets the default PostgreSQL credentials and database:
- **User**: root
- **Password**: root
- **Database**: test_db

## Dependencies
Requires Docker installed on the host machine.

## Building the Docker Image
To build the Docker image, run:

`docker build -t postgres-wal2json .`

## Running the Container
To start a container from the image, use:

`docker run -p 5432:5432 postgres-wal2json`

This command maps port 5432 on the host to port 5432 in the Docker container, enabling database connections from the host to the container.

## Usage
Connect to the PostgreSQL server using standard PostgreSQL client tools or libraries by specifying `host=localhost`, with the user, password, and database provided in the environment variables.


