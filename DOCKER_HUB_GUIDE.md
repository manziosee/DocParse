# Docker Hub Deployment Guide

## Project Information
- **Project**: DocParse - AI-Powered Document Parser API
- **Company**: SMART IT CONSULTING
- **Contact**: manziosee3@gmail.com
- **Year**: 2025

## Build and Push to Docker Hub

### 1. Login to Docker Hub
```bash
docker login
# Username: your-dockerhub-username
# Password: your-dockerhub-password
```

### 2. Build the Image
```bash
docker build -t manziosee3/docparse:latest .
```

### 3. Tag the Image (Optional - for versioning)
```bash
docker tag manziosee3/docparse:latest manziosee3/docparse:v1.0.0
```

### 4. Push to Docker Hub
```bash
docker push manziosee3/docparse:latest
docker push manziosee3/docparse:v1.0.0
```

## Pull and Run from Docker Hub

### Pull the Image
```bash
docker pull manziosee3/docparse:latest
```

### Run the Container
```bash
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-api-key-here \
  --name docparse \
  manziosee3/docparse:latest
```

## Using Docker Compose with Docker Hub Image

Update `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    image: manziosee3/docparse:latest
    volumes:
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

volumes:
  media_volume:
```

Then run:
```bash
docker-compose up -d
```

## Environment Variables

Required:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Access the Application

- API: http://localhost:8000/api/documents/
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin: http://localhost:8000/admin/

## Support

For issues or questions, contact: manziosee3@gmail.com

---
**SMART IT CONSULTING** - 2025
