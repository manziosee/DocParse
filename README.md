# DocParse - AI-Powered Document Parser API

> Professional Django REST API for extracting structured information from documents (PDF, Word, Images) using AI and pattern matching

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- 📄 **Multi-format Support**: PDF, Word (.docx), and image files (JPG, PNG, etc.)
- 🤖 **Dual Extraction Modes**: 
  - AI-powered extraction using OpenAI GPT-4
  - Free pattern-matching extraction (no API costs)
- 🎯 **Custom Field Extraction**: Extract only specific fields you need
- 📋 **Document Types**: Invoices, proforma invoices, receipts, and business documents
- 🔄 **RESTful API**: Built with Django REST Framework
- 📚 **Interactive Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Ready**: Complete containerization support
- 🔍 **OCR Support**: Extract text from images using Tesseract

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [API Usage](#-api-usage)
- [Custom Field Extraction](#-custom-field-extraction)
- [API Endpoints](#-api-endpoints)
- [Documentation](#-documentation)
- [Docker Commands](#-docker-commands)
- [Environment Setup](#-environment-setup)

## 🚀 Quick Start

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
sudo apt-get install tesseract-ocr  # For OCR support
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

## 📖 API Usage

### Standard Document Processing

Upload any document and get comprehensive information extraction:

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
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

## 🎯 Custom Field Extraction

Extract only specific fields you need using our **free pattern-matching engine** (no OpenAI API costs):

### Available Fields

| Field | Description | Example Output |
|-------|-------------|----------------|
| `items` | Product/service line items | `["Product A", "Service B"]` |
| `total` | Total amount | `"$120.00"` |
| `subtotal` | Subtotal amount | `"$100.00"` |
| `name` | Names/contacts | `["John Doe", "ABC Corp"]` |
| `amount` | Monetary amounts | `["$50.00", "$25.99"]` |
| `phone` | Phone numbers | `["+1-555-0123", "555.456.7890"]` |
| `email` | Email addresses | `["contact@company.com"]` |
| `date` | Dates | `["2024-01-15", "Jan 15, 2024"]` |
| `contact` | Contact information | `["John Doe +1-555-0123"]` |

### Usage Examples

**Extract specific fields:**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "custom_fields=items,total,subtotal"
```

**Extract contact information:**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@business_card.jpg" \
  -F "custom_fields=name,phone,email"
```

**Extract amounts and dates:**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@receipt.pdf" \
  -F "custom_fields=amount,date,total"
```

**Custom Fields Response:**
```json
{
  "id": 2,
  "file": "/media/documents/invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {
    "items": ["Product A", "Service B", "Consulting"],
    "total": "$120.00",
    "subtotal": "$100.00"
  },
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed": true
}
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/documents/` | Upload & process document |
| **GET** | `/api/documents/` | List all documents |
| **GET** | `/api/documents/{id}/` | Get document details |
| **PUT** | `/api/documents/{id}/` | Update document |
| **PATCH** | `/api/documents/{id}/` | Partial update document |
| **DELETE** | `/api/documents/{id}/` | Delete document |
| **POST** | `/api/documents/{id}/reprocess/` | Reprocess document |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ | Document file (PDF, DOCX, JPG, PNG) |
| `document_type` | String | ❌ | `invoice`, `proforma`, `receipt`, `other` |
| `custom_fields` | String | ❌ | Comma-separated fields to extract |

## 📚 Documentation

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/swagger/ - Test APIs directly in browser
- **ReDoc**: http://localhost:8000/redoc/ - Clean, readable documentation
- **OpenAPI JSON**: http://localhost:8000/swagger.json - Raw API specification

### Testing Tools
- **Postman Collection**: Import `DocParse_API.postman_collection.json`
- **Admin Panel**: http://localhost:8000/admin/ - Manage documents directly

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up --build

# Create Django superuser
docker-compose exec web python manage.py createsuperuser

# Access container shell
docker-compose exec web bash
```

## ⚙️ Environment Setup

### Required Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Key (optional - only needed for AI extraction)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Django Settings (optional)
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Supported File Formats

**Input Files:**
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

**Document Types:**
- `invoice` - Standard invoices
- `proforma` - Proforma invoices  
- `receipt` - Receipts and purchase records
- `other` - General business documents

## 🔧 Advanced Usage

### Batch Processing
```bash
# Process multiple files
for file in *.pdf; do
  curl -X POST http://localhost:8000/api/documents/ \
    -F "file=@$file" \
    -F "custom_fields=items,total"
done
```

### Python Integration
```python
import requests

# Upload document
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={
            'document_type': 'invoice',
            'custom_fields': 'items,total,subtotal'
        }
    )

result = response.json()
print(f"Extracted: {result['extracted_data']}")
```

### JavaScript/Node.js Integration
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('invoice.pdf'));
form.append('custom_fields', 'items,total,subtotal');

fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: form
})
.then(response => response.json())
.then(data => console.log(data.extracted_data));
```

## 🚨 Troubleshooting

### Common Issues

**Docker permission denied:**
```bash
sudo docker-compose up --build
```

**OCR not working:**
```bash
# Install Tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**OpenAI API errors:**
- Use `custom_fields` parameter for free extraction
- Check API key validity and quota

### Performance Tips

- Use `custom_fields` for faster processing
- Optimize image quality for better OCR results
- Use PDF format when possible for best accuracy

## 📊 Extraction Capabilities

### What DocParse Can Extract

**Financial Information:**
- Invoice numbers and dates
- Line items with quantities and prices
- Subtotals, taxes, and total amounts
- Currency information
- Payment terms and due dates

**Contact Information:**
- Vendor/seller details
- Customer/buyer information
- Phone numbers and email addresses
- Physical addresses
- Tax IDs and business numbers

**Document Metadata:**
- Document type detection
- Issue and due dates
- Reference numbers
- Bank details (when available)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 Company

**SMART IT CONSULTING** - 2025  
Professional Document Processing Solutions

---

## 📞 Support

- 📧 **Email**: manziosee3@gmail.com
- 📖 **Documentation**: http://localhost:8000/swagger/
- 🐳 **Docker Guide**: Available in project files

**Need help?** Check out the interactive [API Documentation](http://localhost:8000/swagger/) or explore the [Postman Collection](DocParse_API.postman_collection.json) for ready-to-use examples.