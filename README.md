# DocParse - AI-Powered Document Parser API

> Django REST API for extracting information from documents (PDF, Word, Images) using OpenAI GPT-4

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)

## Features

- 📄 **Multi-format Support**: PDF, Word (.docx), and image files (JPG, PNG, etc.)
- 🤖 **AI-Powered Extraction**: Uses OpenAI GPT-4 for intelligent information extraction
- 📋 **Document Types**: Invoices, proforma invoices, receipts, and other business documents
- 🔄 **RESTful API**: Built with Django REST Framework
- 🎯 **Auto-Detection**: Automatic document type detection
- 📚 **API Documentation**: Interactive Swagger/OpenAPI documentation
- 🐳 **Docker Ready**: Complete containerization support

## Quick Start

### Using Docker (Recommended)

1. **Clone and configure:**
```bash
git clone <repository-url>
cd DocParse
echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
```

2. **Build and run:**
```bash
docker-compose up --build
```

3. **Access the application:**
- 🌐 **API**: http://localhost:8000/api/documents/
- 📖 **Swagger UI**: http://localhost:8000/swagger/
- 📚 **ReDoc**: http://localhost:8000/redoc/
- ⚙️ **Admin**: http://localhost:8000/admin/

### Manual Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
```

3. **Setup database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Run server:**
```bash
python manage.py runserver
```

## API Usage

### Upload Document
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "document_type=invoice"
```

### Response Example
```json
{
  "id": 1,
  "file": "/media/documents/invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {
    "document_type": "Invoice",
    "document_number": "INV-2024-001",
    "date": "2024-01-15",
    "vendor": {
      "name": "ABC Company",
      "address": "123 Main St",
      "tax_id": "123456789"
    },
    "total_amount": 120.00,
    "currency": "USD"
  },
  "processed": true
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/` | Upload & process document |
| GET | `/api/documents/` | List all documents |
| GET | `/api/documents/{id}/` | Get document details |
| POST | `/api/documents/{id}/reprocess/` | Reprocess document |
| DELETE | `/api/documents/{id}/` | Delete document |

## Supported Formats

### File Types
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

### Document Types
- `invoice` - Standard invoices
- `proforma` - Proforma invoices
- `receipt` - Receipts
- `other` - Other business documents

## Extracted Information

The API intelligently extracts:
- Document type and number
- Issue and due dates
- Vendor/seller information
- Customer/buyer details
- Line items with quantities and prices
- Subtotals, taxes, and total amounts
- Currency and payment terms
- Bank details (when available)

## Documentation

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/swagger/ - Test APIs directly
- **ReDoc**: http://localhost:8000/redoc/ - Clean, readable documentation
- **OpenAPI JSON**: http://localhost:8000/swagger.json - Raw specification

### Testing Tools
- **Postman Collection**: Import `DocParse_API.postman_collection.json`
- **Admin Panel**: http://localhost:8000/admin/ - Manage documents

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Environment Variables

Required in `.env` file:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Requirements

- Python 3.11+
- Django 4.2+
- OpenAI API key with GPT-4 access
- Docker (optional, for containerized deployment)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Company

**SMART IT CONSULTING** - 2025

---

**Need help?** Check out the [API Documentation](http://localhost:8000/swagger/) or [Docker Guide](DOCKER_API_GUIDE.md)

## API Endpoints

### Upload and Process Document
**POST** `/api/documents/`

Upload a document file for processing.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `file`: Document file (PDF, DOCX, or image)
  - `document_type`: (optional) One of: invoice, proforma, receipt, other

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@/path/to/invoice.pdf" \
  -F "document_type=invoice"
```

**Response:**
```json
{
  "id": 1,
  "file": "/media/documents/invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {
    "document_type": "Invoice",
    "document_number": "INV-2024-001",
    "date": "2024-01-15",
    "vendor": {
      "name": "ABC Company",
      "address": "123 Main St",
      "tax_id": "123456789"
    },
    "customer": {
      "name": "XYZ Corp",
      "address": "456 Oak Ave"
    },
    "line_items": [
      {
        "description": "Product A",
        "quantity": 2,
        "unit_price": 50.00,
        "total": 100.00
      }
    ],
    "subtotal": 100.00,
    "tax_amount": 20.00,
    "total_amount": 120.00,
    "currency": "USD"
  },
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed": true
}
```

### List All Documents
**GET** `/api/documents/`

Retrieve all uploaded documents.

### Get Document Details
**GET** `/api/documents/{id}/`

Retrieve a specific document by ID.

### Reprocess Document
**POST** `/api/documents/{id}/reprocess/`

Reprocess an existing document to extract information again.

### Delete Document
**DELETE** `/api/documents/{id}/`

Delete a document.

## Supported File Formats

- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

## Extracted Information

The API attempts to extract:
- Document type (invoice, proforma, receipt, etc.)
- Document number/ID
- Dates (issue date, due date)
- Vendor/Seller information
- Customer/Buyer information
- Line items with quantities and prices
- Totals, subtotals, and tax amounts
- Currency
- Payment terms
- Bank details
- Other relevant information

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to manage documents.

## Testing with Postman

**Import Collection:**
Import `DocParse_API.postman_collection.json` into Postman for pre-configured requests.

**Manual Setup:**
1. Create a new POST request to `http://localhost:8000/api/documents/`
2. Select Body → form-data
3. Add key `file` with type `File` and select your document
4. (Optional) Add key `document_type` with value like `invoice`
5. Send the request

## Notes

- Make sure your OpenAI API key has access to GPT-4 models
- Image processing uses GPT-4 Vision (gpt-4-vision-preview)
- Text extraction uses GPT-4 Turbo (gpt-4-turbo-preview)
- Large files may take longer to process
