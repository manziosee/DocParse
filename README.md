# DocParse - AI-Powered Document Parser API

> Professional Django REST API for extracting structured information from documents (PDF, Word, Images) using AI and natural language prompts - **Works like ChatGPT!**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Features

- 📄 **Multi-format Support**: PDF, Word (.docx), and image files (JPG, PNG, etc.)
- 🤖 **AI-Powered Extraction**: Uses OpenAI GPT-4 with natural language prompts
- 💬 **ChatGPT-Style Interaction**: Upload once, ask unlimited questions about your document
- 📋 **Flexible Document Processing**: Works with any document type
- 🔄 **RESTful API**: Built with Django REST Framework
- 📚 **Interactive Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Ready**: Complete containerization support
- 🔍 **OCR Support**: Extract text from images using Tesseract

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [ChatGPT-Style Usage](#-chatgpt-style-usage)
- [API Endpoints](#-api-endpoints)
- [Example Conversations](#-example-conversations)
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
# Edit .env file with your OpenAI API key and other settings
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

## 💬 ChatGPT-Style Usage

### **Step 1: Upload Your Document**
Upload any document (PDF, Word, Image) to the system:

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -F "file=@invoice.pdf"
```

**Response:**
```json
{
  "id": 1,
  "file": "/media/documents/invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {},
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed": false
}
```

### **Step 2: Start Chatting with Your Document**
Now you can ask unlimited questions about your document:

```bash
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the vendor name and total amount?"}'
```

**Response:**
```json
{
  "prompt": "What is the vendor name and total amount?",
  "response": {
    "vendor_name": "ABC Company Inc.",
    "total_amount": "$1,250.00"
  },
  "document_id": 1
}
```

### **Step 3: Ask More Questions**
Continue the conversation with the same document:

```bash
# Ask about line items
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "List all the line items with their quantities and prices"}'

# Ask about dates
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the invoice date and due date?"}'

# Ask about contact information
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me all contact information including phone numbers and email addresses"}'
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/documents/` | Upload document for processing |
| **GET** | `/api/documents/` | List all uploaded documents |
| **GET** | `/api/documents/{id}/` | Get document details |
| **POST** | `/api/documents/{id}/extract/` | **Chat with document using prompts** |

### Request Parameters

#### Upload Document
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ | Document file (PDF, DOCX, JPG, PNG, etc.) |
| `document_type` | String | ❌ | `invoice`, `proforma`, `receipt`, `other` |

#### Chat with Document
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | String | ✅ | Natural language question about the document |

## 💡 Example Conversations

### **Financial Documents**
```bash
# Upload invoice
curl -X POST http://localhost:8000/api/documents/ -F "file=@invoice.pdf"

# Ask about financial details
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are all the amounts, taxes, and subtotals?"}'

# Ask about payment terms
curl -X POST http://localhost:8000/api/documents/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the payment terms and due date?"}'
```

### **Business Cards**
```bash
# Upload business card image
curl -X POST http://localhost:8000/api/documents/ -F "file=@business_card.jpg"

# Extract contact info
curl -X POST http://localhost:8000/api/documents/2/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the person'\''s name, job title, and company?"}'

# Get contact details
curl -X POST http://localhost:8000/api/documents/2/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me the phone number, email, and website"}'
```

### **Contracts & Legal Documents**
```bash
# Upload contract
curl -X POST http://localhost:8000/api/documents/ -F "file=@contract.pdf"

# Ask about parties
curl -X POST http://localhost:8000/api/documents/3/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Who are the parties involved in this contract?"}'

# Ask about terms
curl -X POST http://localhost:8000/api/documents/3/extract/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the key terms, effective date, and termination clauses?"}'
```

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

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI Configuration (required for AI extraction)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Security Note:** Never commit your `.env` file to version control.

### Supported File Formats

**Input Files:**
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`

**Document Types:**
- Any document type - the AI will automatically detect and process

## 🔧 Advanced Usage

### Python Integration
```python
import requests

# Upload document
with open('invoice.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f}
    )
    document_id = response.json()['id']

# Chat with document
def ask_document(document_id, question):
    response = requests.post(
        f'http://localhost:8000/api/documents/{document_id}/extract/',
        json={'prompt': question}
    )
    return response.json()['response']

# Ask multiple questions
vendor = ask_document(document_id, "What is the vendor name?")
total = ask_document(document_id, "What is the total amount?")
items = ask_document(document_id, "List all line items")
```

### JavaScript/Node.js Integration
```javascript
// Upload document
const formData = new FormData();
formData.append('file', fs.createReadStream('invoice.pdf'));

const uploadResponse = await fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: formData
});
const document = await uploadResponse.json();

// Chat with document
async function askDocument(documentId, question) {
    const response = await fetch(`http://localhost:8000/api/documents/${documentId}/extract/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: question })
    });
    const result = await response.json();
    return result.response;
}

// Ask questions
const vendor = await askDocument(document.id, "What is the vendor name?");
const total = await askDocument(document.id, "What is the total amount?");
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

- Use specific questions for faster, more accurate results
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
- Any information you specify in your prompts
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

## 🎯 Example Questions You Can Ask

Get inspired with these example prompts:

- `"What is the vendor name and total amount?"`
- `"List all line items with their prices and quantities"`
- `"What are the invoice date and due date?"`
- `"Give me all contact information including phone and email"`
- `"What are the payment terms and conditions?"`
- `"Extract all monetary amounts and currency information"`
- `"Who are the parties involved in this document?"`
- `"What are the key terms and important dates?"`
- `"Find all reference numbers and document IDs"`
- `"What technical specifications are mentioned?"`

**The beauty of DocParse is that you can ask anything about your document in natural language, just like ChatGPT!**