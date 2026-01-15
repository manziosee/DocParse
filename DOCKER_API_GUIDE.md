# Docker & API Documentation Guide

## Docker Commands

### Build and Start
```bash
# Build and start containers
docker-compose up --build

# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f
```

### Stop and Clean
```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild from scratch
docker-compose down -v && docker-compose up --build
```

### Execute Commands in Container
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Access shell
docker-compose exec web python manage.py shell

# Access container bash
docker-compose exec web bash
```

## API Documentation URLs

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/swagger/
  - Interactive API documentation
  - Test endpoints directly from browser
  - View request/response schemas

- **ReDoc**: http://localhost:8000/redoc/
  - Clean, readable API documentation
  - Better for reading and understanding

- **OpenAPI JSON**: http://localhost:8000/swagger.json
  - Raw OpenAPI specification
  - Import into Postman, Insomnia, etc.

## Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/swagger/
2. Click on "POST /api/documents/"
3. Click "Try it out"
4. Upload a file and optionally set document_type
5. Click "Execute"
6. View the response

### Using curl
```bash
# Upload a document
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "document_type=invoice"

# List all documents
curl http://localhost:8000/api/documents/

# Get specific document
curl http://localhost:8000/api/documents/1/

# Reprocess document
curl -X POST http://localhost:8000/api/documents/1/reprocess/

# Delete document
curl -X DELETE http://localhost:8000/api/documents/1/
```

### Using Python requests
```python
import requests

# Upload document
url = "http://localhost:8000/api/documents/"
files = {'file': open('invoice.pdf', 'rb')}
data = {'document_type': 'invoice'}
response = requests.post(url, files=files, data=data)
print(response.json())
```

## Environment Variables

Edit `.env` file:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Supported File Types

- PDF: `.pdf`
- Word: `.docx`, `.doc`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

## Supported Document Types

- `invoice` - Standard invoices
- `proforma` - Proforma invoices
- `receipt` - Receipts
- `other` - Other business documents
