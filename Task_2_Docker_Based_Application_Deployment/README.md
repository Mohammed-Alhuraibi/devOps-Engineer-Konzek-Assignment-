# Simple HTTP Server Setup Guide

## Prerequisites

### For Linux-Based Operating Systems:
- Docker
- Docker Compose

### For Windows-Based Operating Systems:
- Docker Desktop

## Instructions to Deploy the Application Locally

1. Navigate to the root folder of the project.
2. Run the following command:
   > **Important:** Make sure port 80 isn't already allocated.

   ```bash
   docker compose up --build
   ```
   - The `--build` flag ensures the image is built locally using the Dockerfile.

## Verifying the Deployment

To verify that the application is running:

- Enter `localhost` in the browser and keep refreshing the page. You'll notice the hostname changes, indicating that load balancing is working.
- Run the following command to see the running services:
  ```bash
  docker ps
  ```
- You should see three services (containers) running:
  - One for NGINX, which is used for load balancing.
  - Two for the simple HTTP servers.

