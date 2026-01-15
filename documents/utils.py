import os
import base64
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from PIL import Image
from io import BytesIO

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    """Extract text from Word document"""
    doc = DocxDocument(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()

def image_to_base64(file_path):
    """Convert image to base64 for OpenAI Vision API"""
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def process_document(file_path, filename):
    """Process document based on file type"""
    ext = get_file_extension(filename)
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path), 'text'
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path), 'text'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return image_to_base64(file_path), 'image'
    else:
        raise ValueError(f"Unsupported file format: {ext}")
