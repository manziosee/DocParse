# DocParse - AI-Powered Document Parser API

> Professional Django REST API for extracting structured information from documents (PDF, Word, Images) using AI and natural language prompts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- 📄 **Multi-format Support**: PDF, Word (.docx), and image files (JPG, PNG, etc.)
- 🤖 **AI-Powered Extraction**: Uses OpenAI GPT-4 with natural language prompts
- 💬 **Natural Language Prompts**: Tell the API exactly what you want to extract
- 📋 **Flexible Document Processing**: Works with any document type
- 🔄 **RESTful API**: Built with Django REST Framework
- 📚 **Interactive Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Ready**: Complete containerization support
- 🔍 **OCR Support**: Extract text from images using Tesseract

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [API Usage](#-api-usage)
- [Prompt Examples](#-prompt-examples)
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

### Basic Document Processing

Upload any document and let AI extract all relevant information:

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf"
```

### Prompt-Based Extraction

Upload a document with a specific prompt describing what you want to extract:

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=Extract vendor name, total amount, and all line items"
```

**Response:**
```json
{
  "id": 1,
  "file": "/media/documents/invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {
    "vendor_name": "ABC Company Inc.",
    "total_amount": "$1,250.00",
    "line_items": [
      {
        "description": "Web Development Services",
        "quantity": 40,
        "unit_price": "$25.00",
        "total": "$1,000.00"
      },
      {
        "description": "Domain Registration",
        "quantity": 1,
        "unit_price": "$15.00", 
        "total": "$15.00"
      }
    ]
  },
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed": true
}
```

## 💬 Prompt Examples

### Financial Documents
```bash
# Extract financial information
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=Extract all amounts, taxes, subtotals, and payment terms"

# Get vendor and customer details
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=Extract vendor information, customer details, and billing addresses"
```

### Contact Information
```bash
# Extract contact details
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@business_card.jpg" \
  -F "prompt=Extract name, phone number, email, company, and job title"

# Get all contact information
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@document.pdf" \
  -F "prompt=Find all phone numbers, email addresses, and physical addresses"
```

### Specific Data Extraction
```bash
# Extract dates and reference numbers
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@contract.pdf" \
  -F "prompt=Extract all dates, reference numbers, and document IDs"

# Get product information
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@catalog.pdf" \
  -F "prompt=Extract product names, prices, and descriptions"
```

### Custom Business Logic
```bash
# Extract specific business data
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@report.pdf" \
  -F "prompt=Extract key performance metrics, revenue figures, and growth percentages"

# Legal document extraction
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@contract.pdf" \
  -F "prompt=Extract party names, contract terms, effective dates, and termination clauses"
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/documents/` | Upload & process document with prompt |
| **GET** | `/api/documents/` | List all documents |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ | Document file (PDF, DOCX, JPG, PNG, etc.) |
| `prompt` | String | ❌ | Natural language prompt describing what to extract |
| `document_type` | String | ❌ | `invoice`, `proforma`, `receipt`, `other` |

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

# Clean restart (if having issues)
docker-compose down -v
docker system prune -f
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
# OpenAI API Key (required for AI extraction)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Django Settings (optional)
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Supported File Formats

**Input Files:**
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`

**Document Types:**
- Any document type - the AI will automatically detect and process

## 🔧 Advanced Usage

### Batch Processing
```bash
# Process multiple files with different prompts
for file in *.pdf; do
  curl -X POST http://localhost:8000/api/documents/ \
    -F "file=@$file" \
    -F "prompt=Extract vendor name and total amount"
done
```

### Python Integration
```python
import requests

# Upload document with custom prompt
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={
            'prompt': 'Extract all contact information and financial details'
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
form.append('file', fs.createReadStream('document.pdf'));
form.append('prompt', 'Extract names, dates, and amounts');

fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: form
})
.then(response => response.json())
.then(data => console.log(data.extracted_data));
```

## 🚨 Troubleshooting

### Common Issues

**Docker ContainerConfig error:**
```bash
# Clean up Docker containers and volumes
docker-compose down -v
docker system prune -f

# Rebuild from scratch
docker-compose up --build
```

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
- Check API key validity and quota
- Ensure OPENAI_API_KEY is set in .env file

### Performance Tips

- Use specific prompts for faster, more accurate results
- Optimize image quality for better OCR results
- Use PDF format when possible for best accuracy

## 📊 Extraction Capabilities

### What DocParse Can Extract

**Financial Information:**
- Invoice numbers and amounts
- Line items with quantities and prices
- Subtotals, taxes, and totals
- Payment terms and due dates
- Currency information

**Contact Information:**
- Names and titles
- Phone numbers and email addresses
- Physical addresses
- Company information
- Tax IDs and business numbers

**Document Metadata:**
- Document type and dates
- Reference numbers
- Signatures and approvals
- Terms and conditions

**Custom Data:**
- Any information you specify in your prompt
- Business-specific fields
- Legal terms and clauses
- Technical specifications

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

## 🎯 Example Prompts

Get inspired with these example prompts:

- `"Extract all contact information including names, phone numbers, and email addresses"`
- `"Get vendor details, line items, and total amount from this invoice"`
- `"Find all dates, reference numbers, and document identifiers"`
- `"Extract product names, prices, and quantities"`
- `"Get customer information and billing details"`
- `"Find all monetary amounts and currency information"`
- `"Extract contract terms, parties involved, and effective dates"`
- `"Get technical specifications and model numbers"`