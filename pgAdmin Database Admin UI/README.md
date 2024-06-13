# pgAdmin Database Admin UI

## Overview
This Docker setup uses the official pgAdmin Docker image to create a ready-to-use pgAdmin instance for testing. [pgAdmin](https://www.pgadmin.org/) is a web-based administration tool for PostgreSQL.

## Features
- **Pre-configured login credentials** for quick access.
- **Exposed on port 80** for easy web access.

## Configuration
The Dockerfile sets the default pgAdmin login credentials:
- **Email**: admin@admin.com
- **Password**: root

## Dependencies
Requires Docker installed on the host machine.

## Building the Docker Image
To build the Docker image, run:

`docker build -t pgadmin-docker .`

## Running the Container
To start a container from the image, use:

`docker run -p 80:80 pgadmin-docker`

This command maps port 80 on the host to port 80 in the Docker container, allowing you to access pgAdmin by visiting `http://localhost` on your web browser.
