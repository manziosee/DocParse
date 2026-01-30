import os
import base64
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from PIL import Image
from io import BytesIO

# Try to import pytesseract, but make it optional
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

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

def extract_text_from_image(file_path):
    """Extract text from image using OCR if available"""
    if OCR_AVAILABLE:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except:
            pass
    # If OCR not available or fails, return base64
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_base64(file_path):
    """Convert image to base64"""
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
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), 'text'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        # Try OCR first if available
        if OCR_AVAILABLE:
            text = extract_text_from_image(file_path)
            if len(text) > 50:  # If OCR extracted meaningful text
                return text, 'text'
        # Otherwise return as image
        return image_to_base64(file_path), 'image'
    else:
        raise ValueError(f"Unsupported file format: {ext}")
