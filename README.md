# DocParse - AI-Powered Document Parser API

> Professional Django REST API for extracting structured information from documents (PDF, Word, Images) using AI and natural language prompts - **Simple Upload & Extract!**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- 📄 **Multi-format Support**: PDF, Word (.docx), and image files (JPG, PNG, etc.)
- 🤖 **AI-Powered Extraction**: Uses OpenAI GPT-4 with natural language prompts
- ⚡ **Instant Results**: Upload document with prompt and get immediate extraction
- 📋 **No ID Management**: Simple upload and extract - no complex workflows
- 🔄 **RESTful API**: Built with Django REST Framework
- 📚 **Interactive Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Ready**: Complete containerization support
- 🔍 **OCR Support**: Extract text from images using Tesseract

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Simple Usage](#-simple-usage)
- [API Endpoints](#-api-endpoints)
- [Example Extractions](#-example-extractions)
- [Documentation](#-documentation)
- [Docker Commands](#-docker-commands)
- [Environment Setup](#-environment-setup)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and configure:**
```bash
git clone <repository-url>
cd DocParse
cp .env.example .env
# Edit .env file with your OpenAI API key
```

2. **Build and run:**
```bash
docker-compose up --build
```

3. **Access the application:**
- 🌐 **API**: http://localhost:8000/api/documents/
- 📖 **Swagger UI**: http://localhost:8000/swagger/
- 📚 **ReDoc**: http://localhost:8000/redoc/

### Manual Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
sudo apt-get install tesseract-ocr  # For OCR support
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env file with your OpenAI API key
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

## ⚡ Simple Usage

### **Upload Document + Extract Information (One Step!)**

Upload any document with your prompt and get instant results:

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@your_document.pdf" \
  -F "prompt=List all the line items with their quantities and prices"
```

**Response:**
```json
{
  "prompt": "List all the line items with their quantities and prices",
  "response": {
    "line_items": [
      {
        "item": "Office Chair",
        "quantity": 2,
        "unit_price": "RWF 75,000",
        "total": "RWF 150,000"
      },
      {
        "item": "Desk Lamp",
        "quantity": 5,
        "unit_price": "RWF 15,000",
        "total": "RWF 75,000"
      },
      {
        "item": "Filing Cabinet",
        "quantity": 1,
        "unit_price": "RWF 120,000",
        "total": "RWF 120,000"
      }
    ]
  }
}
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/documents/` | Upload document + extract with prompt |
| **GET** | `/api/documents/` | List all uploaded documents |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ | Document file (PDF, DOCX, JPG, PNG, etc.) |
| `prompt` | String | ✅ | Natural language question about the document |
| `document_type` | String | ❌ | `invoice`, `proforma`, `receipt`, `other` |

## 💡 Example Extractions

### **Financial Documents**
```bash
# Extract line items
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=List all the line items with their quantities and prices"

# Extract vendor and total
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=What is the vendor name and total amount?"

# Extract payment terms
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=What are the payment terms and due date?"
```

### **Business Cards**
```bash
# Extract contact info
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@business_card.jpg" \
  -F "prompt=Extract name, phone number, email, and company"
```

### **Contracts & Legal Documents**
```bash
# Extract parties and terms
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@contract.pdf" \
  -F "prompt=Who are the parties involved and what are the key terms?"
```

## 📚 Documentation

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/swagger/ - Test APIs directly in browser
- **ReDoc**: http://localhost:8000/redoc/ - Clean, readable documentation
- **OpenAPI JSON**: http://localhost:8000/swagger.json - Raw API specification

### Testing Tools
- **Postman Collection**: Import `DocParse_API.postman_collection.json`

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
```

## ⚙️ Environment Setup

### Required Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI Configuration (required for AI extraction)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Supported File Formats

**Input Files:**
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`

## 🔧 Advanced Usage

### Python Integration
```python
import requests

# Upload and extract in one call
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={'prompt': 'List all line items with quantities and prices'}
    )

result = response.json()
print(f"Extracted: {result['response']}")
```

### JavaScript/Node.js Integration
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('invoice.pdf'));
form.append('prompt', 'What is the vendor name and total amount?');

fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: form
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## 🚨 Troubleshooting

### Common Issues

**Docker ContainerConfig error:**
```bash
# Clean up Docker containers and volumes
docker-compose down -v
docker system prune -f
docker-compose up --build
```

**Docker permission denied:**
```bash
sudo docker-compose up --build
```

**OpenAI API errors:**
- Check API key validity and quota
- Ensure OPENAI_API_KEY is set in .env file

### Performance Tips

- Use specific prompts for faster, more accurate results
- Optimize image quality for better OCR results
- Use PDF format when possible for best accuracy

## 📊 What DocParse Can Extract

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

## 🎯 Example Prompts

Get inspired with these example prompts:

- `"List all the line items with their quantities and prices"`
- `"What is the vendor name and total amount?"`
- `"What are the invoice date and due date?"`
- `"Extract all contact information including phone and email"`
- `"What are the payment terms and conditions?"`
- `"Extract all monetary amounts and currency information"`
- `"Who are the parties involved in this document?"`
- `"What are the key terms and important dates?"`
- `"Find all reference numbers and document IDs"`

**Simple and powerful - just upload your document with a prompt and get instant results!**