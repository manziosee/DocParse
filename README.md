# DocParse - AI-Powered Document Parser API

> Professional Django REST API for extracting structured information from documents (PDF, Word, Images) using AI and natural language prompts - **Simple Upload & Extract!**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- 📄 **Multi-format Support**: PDF, Word (.docx), Text (.txt), and image files (JPG, PNG, etc.)
- 🤖 **AI-Powered Extraction**: Uses OpenAI GPT with natural language prompts
- ⚡ **Instant Results**: Upload document with optional prompt and get immediate extraction
- 📋 **No Complex Workflows**: Single endpoint - upload and extract in one step
- 🔄 **RESTful API**: Built with Django REST Framework
- 📚 **Interactive Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Ready**: Complete containerization support
- 🔍 **OCR Support**: Extract text from images using Tesseract

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Simple Usage](#-simple-usage)
- [API Endpoint](#-api-endpoint)
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

### **Upload Document & Extract Information (One Endpoint!)**

Upload any document with optional prompt and get instant results:

**With specific prompt:**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@your_document.pdf" \
  -F "prompt=What is the total amount?"
```

**Response:**
```json
{
  "total_amount": "RWF 654,900"
}
```

**Without prompt (extracts everything):**
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{
  "dates": ["2024-01-15"],
  "amounts": ["RWF 654,900", "RWF 120,000"],
  "names": ["John Smith"],
  "companies": ["ABC Supplies Ltd"],
  "emails": ["john@abc.com"]
}
```

## 🔗 API Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/documents/` | Upload document & extract with optional prompt |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ | Document file (PDF, DOCX, TXT, JPG, PNG, etc.) |
| `prompt` | String | ❌ | Natural language question about the document |
| `document_type` | String | ❌ | `invoice`, `proforma`, `receipt`, `other` |

## 💡 Example Extractions

### **Specific Information**
```bash
# Extract total amount only
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=What is the total amount?"

# Extract names only
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=Get me the names of people in this document"

# Extract invoice date
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=What is the invoice date?"
```

### **All Information**
```bash
# Extract everything (no prompt)
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf"
```

### **Business Cards**
```bash
# Extract contact info
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@business_card.jpg" \
  -F "prompt=Extract name, phone number, email, and company"
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
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### Supported File Formats

**Input Files:**
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Text**: `.txt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`

## 🔧 Advanced Usage

### Python Integration
```python
import requests

# Upload and extract with specific prompt
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={'prompt': 'What is the total amount?'}
    )

result = response.json()
print(f"Total: {result.get('total_amount')}")

# Upload and extract everything (no prompt)
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f}
    )

result = response.json()
print(f"All data: {result}")
```

### JavaScript/Node.js Integration
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('invoice.pdf'));
form.append('prompt', 'What is the total amount?');

fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: form
})
.then(response => response.json())
.then(data => console.log(data));
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

**OpenAI API errors:**
- Check API key validity and quota
- Ensure OPENAI_API_KEY is set in .env file
- Verify you have credits in your OpenAI account

### Performance Tips

- Use specific prompts for faster, more accurate results
- Optimize image quality for better OCR results
- Use PDF format when possible for best accuracy

## 📊 What DocParse Can Extract

**With Specific Prompts:**
- Any information you ask for in natural language
- Financial data (amounts, totals, line items)
- Contact information (names, emails, phones)
- Dates and reference numbers
- Custom business data

**Without Prompt (Extracts All):**
- All dates found in document
- All monetary amounts
- All person names
- All company names
- All email addresses

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

- `"What is the total amount?"`
- `"Get me the names of people in this document"`
- `"What is the invoice date?"`
- `"Extract all contact information"`
- `"What are the line items?"`
- `"Find all monetary amounts"`
- `"Who are the companies mentioned?"`
- `"What are the key dates?"`
- `"Extract email addresses"`

**Or leave prompt empty to extract everything automatically!**

**Simple and powerful - just upload your document and get instant results!**