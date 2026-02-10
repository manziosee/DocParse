from django.conf import settings
import logging
import re
import json
import base64
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Available OpenAI models in order of preference
OPENAI_MODELS = [
    "gpt-3.5-turbo",   # Free tier available
    "gpt-4o-mini",     # Paid tier
    "gpt-4o",          # Paid tier
]

def get_working_model():
    """Get the OpenAI model to use."""
    if hasattr(settings, 'OPENAI_MODEL') and settings.OPENAI_MODEL:
        return settings.OPENAI_MODEL
    return OPENAI_MODELS[0]

def sanitize_prompt(prompt: str) -> str:
    """Sanitize user prompt to prevent injection."""
    if not prompt or not isinstance(prompt, str):
        return "Extract all information from this document"
    
    # Remove potentially dangerous characters and limit length
    sanitized = re.sub(r'[<>{}\\]', '', prompt.strip())
    return sanitized[:500]  # Limit prompt length

def validate_file_path(file_path: str) -> bool:
    """Validate file path to prevent traversal attacks."""
    if not file_path or not isinstance(file_path, str):
        return False
    
    # Resolve path and check if it's within allowed directory
    try:
        resolved_path = os.path.realpath(file_path)
        media_root = os.path.realpath(settings.MEDIA_ROOT)
        return resolved_path.startswith(media_root)
    except:
        return False

def clean_json_response(data):
    """Recursively clean all strings in JSON response."""
    if isinstance(data, dict):
        return {key: clean_json_response(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_json_response(item) for item in data]
    elif isinstance(data, str):
        # Remove all newlines, tabs, and normalize whitespace
        cleaned = re.sub(r'[\n\r\t]+', ' ', data)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    return data

def extract_info_with_prompt(content: str, prompt: str = "") -> dict:
    """Extract information from document content using advanced AI analysis."""
    try:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return advanced_fallback_extraction(content, prompt)

        try:
            from openai import OpenAI
        except ImportError:
            return advanced_fallback_extraction(content, prompt)

        sanitized_prompt = sanitize_prompt(prompt)
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        model = get_working_model()

        # Enhanced system prompt for comprehensive analysis
        system_prompt = """You are a document extraction AI. Extract information from documents and return clean, structured JSON.

Rules:
1. Use descriptive keys based on what you find in the document
2. Group related data logically
3. Return actual values from the document, not placeholders
4. Clean all text - remove extra whitespace and newlines
5. Return only valid JSON, no markdown or explanations"""

        # Enhanced user prompt based on request
        if not sanitized_prompt or sanitized_prompt == "Extract all information from this document":
            user_prompt = f"""Extract ALL information from this document and return as clean JSON.
            
Document Content:
{content[:3500]}

Return clean, well-structured JSON with all information you find."""
        else:
            user_prompt = f"""{sanitized_prompt}

Document Content:
{content[:3500]}

Extract the requested information and return as clean JSON."""

        response = client.chat.completions.create(
            model=model,
            max_tokens=2000,
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        
        try:
            parsed = json.loads(result)
            return clean_json_response(parsed)
        except json.JSONDecodeError:
            return {"extracted_information": result}

    except Exception as e:
        return advanced_fallback_extraction(content, prompt)

def advanced_fallback_extraction(content: str, prompt: str = "") -> dict:
    """Advanced pattern-based extraction - returns clean data without hardcoded structure."""
    result = {}
    
    # Extract all data
    financial_data = extract_financial_info(content)
    contact_data = extract_contact_info(content)
    business_data = extract_business_info(content)
    metadata = extract_document_metadata(content)
    structured_data = extract_structured_content(content)
    
    # Merge all extracted data
    result.update(financial_data)
    result.update(contact_data)
    result.update(business_data)
    result.update(metadata)
    result.update(structured_data)
    
    # Clean the entire result
    return clean_json_response(result) if result else {"message": "No information extracted"}

def extract_financial_info(content: str) -> dict:
    """Extract financial information."""
    financial = {}
    
    # Currency amounts
    amounts = re.findall(r'(?:RWF|USD|EUR|GBP|\$|\u20ac|\u00a3)\s*[\d,]+(?:\.\d{2})?|[\d,]+(?:\.\d{2})?\s*(?:RWF|USD|EUR|GBP)', content, re.IGNORECASE)
    if amounts:
        financial["amounts"] = list(set(amounts))
    
    # Percentages
    percentages = re.findall(r'\d+(?:\.\d+)?%', content)
    if percentages:
        financial["percentages"] = list(set(percentages))
    
    return financial

def extract_contact_info(content: str) -> dict:
    """Extract contact information."""
    contact = {}
    
    # Email addresses
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    if emails:
        contact["emails"] = list(set(emails))
    
    # Phone numbers
    phones = re.findall(r'(?:\+?\d{1,4}[\s\-\.]?)?\(?\d{3,4}\)?[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}', content)
    if phones:
        contact["phones"] = list(set(phones))
    
    # Addresses
    addresses = re.findall(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[^\n]*', content, re.IGNORECASE)
    if addresses:
        contact["addresses"] = list(set(addresses))
    
    # Names
    names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', content)
    if names:
        contact["names"] = list(set(names))
    
    return contact

def extract_business_info(content: str) -> dict:
    """Extract business information."""
    business = {}
    
    # Company names
    companies = re.findall(r'[A-Z][A-Za-z\s&]+(?:Ltd|Inc|Corp|LLC|Limited|Company|Corporation|Co\.|Pty|GmbH|SA|SAS)', content)
    if companies:
        business["companies"] = list(set(companies))
    
    return business

def extract_document_metadata(content: str) -> dict:
    """Extract document metadata."""
    metadata = {}
    
    # Dates
    dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}', content, re.IGNORECASE)
    if dates:
        metadata["dates"] = list(set(dates))
    
    # Reference numbers
    refs = re.findall(r'(?:invoice|receipt|order|ref|reference|doc|document)\s*#?:?\s*([A-Z0-9\-]+)', content, re.IGNORECASE)
    if refs:
        metadata["references"] = list(set(refs))
    
    return metadata

def extract_structured_content(content: str) -> dict:
    """Extract structured content."""
    structured = {}
    
    # URLs
    urls = re.findall(r'https?://[^\s]+|www\.[^\s]+', content)
    if urls:
        structured["urls"] = list(set(urls))
    
    return structured



def extract_info_from_image(image_path: str, prompt: str = "") -> dict:
    """Extract comprehensive information from images using advanced AI vision."""
    try:
        if not validate_file_path(image_path):
            return {"error": "Invalid file path"}
            
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return {"error": "OpenAI API key not configured"}

        try:
            from openai import OpenAI
        except ImportError:
            return {"error": "OpenAI library not available"}

        with open(image_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')

        image_type = "jpeg"
        if image_path.lower().endswith('.png'):
            image_type = "png"
        elif image_path.lower().endswith('.gif'):
            image_type = "gif"
        elif image_path.lower().endswith('.webp'):
            image_type = "webp"

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        model = get_working_model()
        
        if "gpt-3.5" in model:
            return {"error": "Image processing requires GPT-4 models"}

        sanitized_prompt = sanitize_prompt(prompt)

        # Enhanced vision analysis prompt
        if not sanitized_prompt or sanitized_prompt == "Extract all information from this document":
            vision_prompt = """Extract ALL information from this image/document and return as clean JSON. Use actual values from the document."""
        else:
            vision_prompt = f"{sanitized_prompt}\n\nExtract the requested information from the image and return as clean JSON with actual values."

        response = client.chat.completions.create(
            model=model,
            max_tokens=2000,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": vision_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_type};base64,{image_data}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
        )

        result = response.choices[0].message.content.strip()
        
        try:
            parsed = json.loads(result)
            return clean_json_response(parsed)
        except json.JSONDecodeError:
            return {"extracted_information": result}

    except Exception as e:
        return {"error": f"Image extraction failed: {str(e)}"}