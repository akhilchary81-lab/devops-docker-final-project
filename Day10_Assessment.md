# Day 10 Docker Knowledge Assessment


# 1. Basic Docker

## 1.1 What is Docker?

Docker is a platform used to package an application along with its dependencies, libraries, and configuration into a container. This allows the application to run consistently in different environments.

For example:

1. A Python application can run inside a Docker container without manually installing Python and dependencies on every server.
2. A Node.js application can be packaged as a Docker image and deployed to development, testing, and production environments.

---

## 1.2 What is a Container?

A container is a running instance of a Docker image.

It contains the application and everything required to run it, while remaining isolated from other containers.

For example:

1. A PostgreSQL Docker image becomes a PostgreSQL container when started.
2. A Python application image becomes a running web application container.

Example command:

```bash
docker run nginx
```

This creates and starts a container using the Nginx image.

---

## 1.3 What is a Docker Image?

A Docker image is a packaged template used to create containers.

An image contains:

* Application code
* Dependencies
* Libraries
* Runtime
* Configuration
* Startup instructions

For example:

1. `python:3.12-slim` is a Docker image containing Python.
2. `postgres:16-alpine` is a Docker image containing PostgreSQL.

Example:

```bash
docker pull python:3.12-slim
```

---

## 1.4 What is Docker Hub?

Docker Hub is an online container image registry.

It allows users and organizations to:

* Download images
* Upload images
* Share images
* Store different versions of images

For example:

```bash
docker pull nginx
```

Downloads the Nginx image from Docker Hub.

Another example:

```bash
docker pull postgres:16-alpine
```

Downloads the PostgreSQL image.

---

## 1.5 Difference Between an Image and a Container

| Docker Image              | Docker Container                 |
| ------------------------- | -------------------------------- |
| Template or blueprint     | Running instance                 |
| Read-only                 | Can have runtime changes         |
| Used to create containers | Created from an image            |
| Example: `nginx`          | Example: running Nginx container |

Example 1:

```text
Python Image
     ↓
Docker Run
     ↓
Python Container
```

Example 2:

One Docker image can create multiple containers.

```text
nginx Image
   │
   ├── Container 1
   ├── Container 2
   └── Container 3
```

---

# 2. Dockerfile

## 2.1 What is a Dockerfile?

A Dockerfile is a text file containing instructions used by Docker to build an image.

A Dockerfile can define:

* Base image
* Working directory
* Dependencies
* Application files
* Environment configuration
* Port
* Startup command

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t devops-final:v1 .
```

---

## 2.2 What Does FROM Do?

The `FROM` instruction specifies the base image.

Example 1:

```dockerfile
FROM python:3.12-slim
```

This starts the image using Python.

Example 2:

```dockerfile
FROM node:20-alpine
```

This starts the image using Node.js.

---

## 2.3 What Does COPY Do?

The `COPY` instruction copies files from the local machine into the Docker image.

Example 1:

```dockerfile
COPY requirements.txt .
```

This copies the dependency file.

Example 2:

```dockerfile
COPY app/ /app/
```

This copies application files into the image.

---

## 2.4 What Does RUN Do?

The `RUN` instruction executes a command while building the Docker image.

Example 1:

```dockerfile
RUN pip install -r requirements.txt
```

This installs Python dependencies.

Example 2:

```dockerfile
RUN apt-get update && apt-get install -y curl
```

This installs the `curl` package.

---

## 2.5 What Does CMD Do?

The `CMD` instruction specifies the default command that runs when the container starts.

Example 1:

```dockerfile
CMD ["python", "app.py"]
```

Example 2:

```dockerfile
CMD ["npm", "start"]
```

The command can be overridden when starting the container.

---

# 3. Docker Compose

## 3.1 What is Docker Compose?

Docker Compose is a tool used to define and run multiple Docker containers using a single configuration file called:

```text
docker-compose.yml
```

For example, an application may require:

```text
Application Container
        │
        ↓
Docker Network
        │
        ↓
PostgreSQL Container
```

Instead of manually running multiple `docker run` commands, Docker Compose manages everything.

Example:

```bash
docker compose up -d
```

---

## 3.2 What is a Service?

A service is a container configuration defined in the `docker-compose.yml` file.

Example:

```yaml
services:
  app:
    image: devops-final:v1

  database:
    image: postgres:16-alpine
```

In this project, there are two services:

1. `app`
2. `database`

---

## 3.3 What is a Compose Network?

A Docker Compose network allows containers to communicate with each other.

For example:

```text
Application
     │
     │ DATABASE_HOST=database
     ↓
Docker Network
     ↓
PostgreSQL
```

The application does not need to know the database container IP address.

It can connect using the service name:

```text
database
```

Example:

```yaml
networks:
  devops-network:
    driver: bridge
```

---

## 3.4 Why Use .env?

The `.env` file stores environment-specific configuration.

It helps separate configuration from application code.

Example:

```env
DATABASE_NAME=devopsdb
DATABASE_USER=devopsuser
DATABASE_PASSWORD=DevOpsPassword123
DATABASE_HOST=database
DATABASE_PORT=5432
```

Examples of what can be stored:

1. Database configuration.
2. Application environment and ports.

Important: Real `.env` files containing secrets should not be committed to GitHub.

---

## 3.5 Why Use .dockerignore?

The `.dockerignore` file prevents unnecessary files from being copied into a Docker image.

Example:

```text
.git
.env
__pycache__
*.pyc
venv/
```

Benefits:

* Smaller Docker images.
* Faster builds.
* Prevent accidental inclusion of secrets.
* Prevent unnecessary files from entering the image.

Example 1:

Do not copy `.git` into the image.

Example 2:

Do not copy local Python virtual environments.

---

# 4. Docker Storage

## 4.1 What is a Docker Volume?

A Docker volume is persistent storage managed by Docker.

It is commonly used for databases.

Example:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

In this project:

```text
PostgreSQL Container
        │
        ↓
Docker Volume
        │
        ↓
Persistent Database Data
```

---

## 4.2 Why Do We Need Volumes?

Containers can be removed and recreated.

Without persistent storage, important data may be lost.

A Docker volume allows data to remain available after the container is removed.

Example 1:

PostgreSQL database data survives container recreation.

Example 2:

Application-generated files can remain available after a new container is deployed.

---

## 4.3 What Happens to Container Data When the Container is Removed?

Data stored only inside the container filesystem is normally removed when the container is deleted.

Example:

```bash
docker rm postgres-container
```

If no Docker volume was configured, the database data can be lost.

With a named volume:

```text
PostgreSQL Container Removed
          │
          ↓
Docker Volume Still Exists
          │
          ↓
Database Data Preserved
```

Example command:

```bash
docker volume ls
```

---

# 5. Docker Troubleshooting

## 5.1 How Do You Check Container Logs?

To check logs for a specific container:

```bash
docker logs <container-name>
```

Example:

```bash
docker logs devops-training-app
```

Using Docker Compose:

```bash
docker compose logs app
```

To continuously monitor logs:

```bash
docker compose logs -f app
```

Example 1:

Check application errors.

Example 2:

Check PostgreSQL startup errors.

---

## 5.2 How Do You Find Why a Container Stopped?

First check all containers:

```bash
docker ps -a
```

Then check logs:

```bash
docker logs <container-name>
```

Inspect the container:

```bash
docker inspect <container-name>
```

Using Docker Compose:

```bash
docker compose ps
```

Example troubleshooting process:

```text
Container Stopped
       ↓
Check Status
       ↓
Check Exit Code
       ↓
Check Logs
       ↓
Inspect Configuration
       ↓
Find Root Cause
       ↓
Fix
       ↓
Restart
       ↓
Test
```

---

# 6. Important Docker Commands

## Check Running Containers

```bash
docker ps
```

## Check All Containers

```bash
docker ps -a
```

## Check Images

```bash
docker images
```

## Build an Image

```bash
docker build -t devops-final:v1 .
```

## Start Docker Compose

```bash
docker compose up -d
```

## Build and Start

```bash
docker compose up -d --build
```

## Stop Containers

```bash
docker compose down
```

## Check Compose Status

```bash
docker compose ps
```

## Check Application Logs

```bash
docker compose logs app
```

## Check Database Logs

```bash
docker compose logs database
```

## Check Networks

```bash
docker network ls
```

## Inspect a Network

```bash
docker network inspect <network-name>
```

## Check Volumes

```bash
docker volume ls
```

## Inspect a Volume

```bash
docker volume inspect <volume-name>
```

---

# 7. Docker Troubleshooting Process

For any problem, the following process should be followed.

```text
Problem
   ↓
Observe
   ↓
Check Status
   ↓
Check Logs
   ↓
Inspect Configuration
   ↓
Find Root Cause
   ↓
Fix
   ↓
Restart
   ↓
Test
```

## Example 1 — Database Connection Failure

### Problem

The application cannot connect to PostgreSQL.

### Observe

The `/health` endpoint returns:

```text
503 Service Unavailable
```

### Check Status

```bash
docker compose ps
```

### Check Logs

```bash
docker compose logs app
```

### Inspect Configuration

```bash
docker compose config
```

Check:

```text
DATABASE_HOST
DATABASE_USER
DATABASE_PASSWORD
DATABASE_PORT
```

### Root Cause

The database password or hostname may be incorrect.

### Fix

Correct the configuration.

### Restart

```bash
docker compose up -d
```

### Test

```bash
curl http://localhost:8080/health
```

---

## Example 2 — Application Container Stops

### Problem

The application is not running.

### Observe

```bash
docker ps
```

The application container is not listed.

### Check Status

```bash
docker ps -a
```

The container may show:

```text
Exited (1)
```

### Check Logs

```bash
docker logs devops-training-app
```

### Inspect Configuration

Check:

```bash
docker inspect devops-training-app
```

Check the Dockerfile startup command.

### Root Cause

The startup command may reference a missing file or invalid command.

### Fix

Correct the Dockerfile.

Example:

```dockerfile
CMD ["python", "app.py"]
```

### Restart

Rebuild the image:

```bash
docker compose up -d --build
```

### Test

```bash
docker compose ps
curl http://localhost:8080/health


# 8. Final Understanding

The complete Docker workflow for this project is:


Write Application
       ↓
Create Dockerfile
       ↓
Build Docker Image
       ↓
Create Docker Compose
       ↓
Configure Application
       ↓
Configure PostgreSQL
       ↓
Create Network
       ↓
Create Named Volume
       ↓
Start Containers
       ↓
Check Container Status
       ↓
Check Logs
       ↓
Test Application
       ↓
Test Health Endpoint
       ↓
Test Database Connectivity
       ↓
Test Persistence
       ↓
Simulate Failure
       ↓
Find Root Cause
       ↓
Fix Problem
       ↓
Restart
       ↓
Verify Application
       ↓
Commit Changes
       ↓
Push to GitHub





