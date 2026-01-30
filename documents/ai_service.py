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
        system_prompt = """You are an expert document analyzer. Extract information accurately and comprehensively.
        Return results as clean JSON. Be thorough and precise. Extract all relevant data including:
        - Financial information (amounts, totals, taxes, discounts)
        - Personal information (names, addresses, contact details)
        - Business information (companies, departments, roles)
        - Document metadata (dates, numbers, references)
        - Content structure (tables, lists, sections)
        - Any other relevant information found in the document"""

        # Enhanced user prompt based on request
        if not sanitized_prompt or sanitized_prompt == "Extract all information from this document":
            user_prompt = f"""Analyze this document comprehensively and extract ALL information including:
            
            FINANCIAL DATA:
            - All monetary amounts, totals, subtotals, taxes, discounts
            - Currency types and payment information
            - Line items with quantities, prices, descriptions
            
            PERSONAL & CONTACT INFO:
            - Names of people, titles, roles
            - Addresses (billing, shipping, business)
            - Phone numbers, email addresses, websites
            
            BUSINESS INFORMATION:
            - Company names, departments, divisions
            - Business registration numbers, tax IDs
            - Industry-specific identifiers
            
            DOCUMENT DETAILS:
            - All dates (creation, due, delivery, etc.)
            - Document numbers, reference codes, IDs
            - Document type and purpose
            
            CONTENT STRUCTURE:
            - Tables, lists, sections, headers
            - Terms and conditions, notes, comments
            - Any other structured or unstructured data
            
            Document Content:
            {content[:3500]}
            
            Return comprehensive JSON with all extracted information organized by category."""
        else:
            user_prompt = f"""{sanitized_prompt}
            
            Document Content:
            {content[:3500]}
            
            Analyze thoroughly and return accurate JSON results."""

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
            return json.loads(result)
        except json.JSONDecodeError:
            return {"extracted_information": result}

    except Exception as e:
        return advanced_fallback_extraction(content, prompt)

def advanced_fallback_extraction(content: str, prompt: str = "") -> dict:
    """Advanced pattern-based extraction for comprehensive document analysis."""
    def clean_value(value):
        if isinstance(value, str):
            return re.sub(r'\s+', ' ', value).strip()
        return value
    
    result = {}
    
    # Extract all financial information
    financial_data = extract_financial_info(content)
    if financial_data:
        result.update(financial_data)
    
    # Extract all contact and personal information
    contact_data = extract_contact_info(content)
    if contact_data:
        result.update(contact_data)
    
    # Extract business and organizational information
    business_data = extract_business_info(content)
    if business_data:
        result.update(business_data)
    
    # Extract document metadata
    metadata = extract_document_metadata(content)
    if metadata:
        result.update(metadata)
    
    # Extract structured content
    structured_data = extract_structured_content(content)
    if structured_data:
        result.update(structured_data)
    
    # If specific prompt provided, filter results
    if prompt.strip():
        result = filter_by_prompt(result, prompt)
    
    return result if result else {"message": "No information extracted"}

def extract_financial_info(content: str) -> dict:
    """Extract comprehensive financial information."""
    financial = {}
    
    # Currency amounts with various formats
    amounts = re.findall(r'(?:RWF|USD|EUR|GBP|\$|\u20ac|\u00a3)\s*[\d,]+(?:\.d{2})?|[\d,]+(?:\.\d{2})?\s*(?:RWF|USD|EUR|GBP)', content, re.IGNORECASE)
    if amounts:
        financial["monetary_amounts"] = [re.sub(r'\s+', ' ', amt).strip() for amt in amounts]
    
    # Percentages (tax rates, discounts)
    percentages = re.findall(r'\d+(?:\.\d+)?%', content)
    if percentages:
        financial["percentages"] = percentages
    
    # Account numbers
    account_numbers = re.findall(r'(?:account|acc|a/c)\s*:?\s*([\d\-\s]+)', content, re.IGNORECASE)
    if account_numbers:
        financial["account_numbers"] = [re.sub(r'\s+', '', acc) for acc in account_numbers]
    
    # Invoice/receipt totals
    totals = re.findall(r'(?:total|grand total|amount due|balance)\s*:?\s*([\d,]+(?:\.\d{2})?)', content, re.IGNORECASE)
    if totals:
        financial["totals"] = totals
    
    return financial

def extract_contact_info(content: str) -> dict:
    """Extract comprehensive contact information."""
    contact = {}
    
    # Email addresses
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    if emails:
        contact["emails"] = emails
    
    # Phone numbers (various formats)
    phones = re.findall(r'(?:\+?\d{1,4}[\s\-\.]?)?\(?\d{3,4}\)?[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}', content)
    if phones:
        contact["phone_numbers"] = [re.sub(r'\s+', ' ', phone).strip() for phone in phones]
    
    # Addresses (multi-line)
    addresses = re.findall(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[^\n]*', content, re.IGNORECASE)
    if addresses:
        contact["addresses"] = [addr.strip() for addr in addresses]
    
    # Postal codes
    postal_codes = re.findall(r'\b\d{5}(?:-\d{4})?\b|\b[A-Z]\d[A-Z]\s?\d[A-Z]\d\b', content)
    if postal_codes:
        contact["postal_codes"] = postal_codes
    
    # Names (improved pattern)
    names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', content)
    # Filter out common non-names
    filtered_names = [name for name in names if not any(word in name.lower() for word in ['street', 'avenue', 'road', 'drive', 'limited', 'company', 'corporation'])]
    if filtered_names:
        contact["names"] = list(set(filtered_names))
    
    return contact

def extract_business_info(content: str) -> dict:
    """Extract business and organizational information."""
    business = {}
    
    # Company names
    companies = re.findall(r'[A-Z][A-Za-z\s&]+(?:Ltd|Inc|Corp|LLC|Limited|Company|Corporation|Co\.|Pty|GmbH|SA|SAS)', content)
    if companies:
        business["companies"] = [comp.strip() for comp in companies]
    
    # Tax IDs and registration numbers
    tax_ids = re.findall(r'(?:tax id|tin|vat|registration)\s*:?\s*([A-Z0-9\-]+)', content, re.IGNORECASE)
    if tax_ids:
        business["tax_identifiers"] = tax_ids
    
    # Departments and divisions
    departments = re.findall(r'(?:department|dept|division|div)\s*:?\s*([A-Za-z\s]+)', content, re.IGNORECASE)
    if departments:
        business["departments"] = [dept.strip() for dept in departments]
    
    return business

def extract_document_metadata(content: str) -> dict:
    """Extract document metadata and references."""
    metadata = {}
    
    # Dates (multiple formats)
    dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}', content, re.IGNORECASE)
    if dates:
        metadata["dates"] = list(set(dates))
    
    # Document numbers and references
    doc_numbers = re.findall(r'(?:invoice|receipt|order|ref|reference|doc|document)\s*#?:?\s*([A-Z0-9\-]+)', content, re.IGNORECASE)
    if doc_numbers:
        metadata["document_numbers"] = doc_numbers
    
    # Serial numbers and IDs
    serial_numbers = re.findall(r'(?:serial|s/n|id|number)\s*:?\s*([A-Z0-9\-]+)', content, re.IGNORECASE)
    if serial_numbers:
        metadata["serial_numbers"] = serial_numbers
    
    return metadata

def extract_structured_content(content: str) -> dict:
    """Extract structured content like tables and lists."""
    structured = {}
    
    # Line items (table-like structure)
    lines = content.split('\n')
    line_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Look for item patterns: description + quantity + price
        item_match = re.search(r'([A-Za-z][^\d]*?)\s+(\d+)\s+([\d,]+(?:\.\d{2})?)\s+([\d,]+(?:\.\d{2})?)', line)
        if item_match:
            line_items.append({
                "description": item_match.group(1).strip(),
                "quantity": item_match.group(2),
                "unit_price": item_match.group(3),
                "total": item_match.group(4)
            })
    
    if line_items:
        structured["line_items"] = line_items
    
    # URLs and websites
    urls = re.findall(r'https?://[^\s]+|www\.[^\s]+', content)
    if urls:
        structured["urls"] = urls
    
    return structured

def filter_by_prompt(data: dict, prompt: str) -> dict:
    """Filter extracted data based on user prompt."""
    prompt_lower = prompt.lower()
    filtered = {}
    
    # Map prompt keywords to data keys
    keyword_mapping = {
        'amount': ['monetary_amounts', 'totals'],
        'total': ['totals', 'monetary_amounts'],
        'money': ['monetary_amounts', 'totals'],
        'price': ['monetary_amounts', 'line_items'],
        'date': ['dates'],
        'name': ['names'],
        'email': ['emails'],
        'phone': ['phone_numbers'],
        'address': ['addresses'],
        'company': ['companies'],
        'business': ['companies', 'departments'],
        'contact': ['emails', 'phone_numbers', 'addresses', 'names'],
        'item': ['line_items'],
        'line': ['line_items'],
        'number': ['document_numbers', 'serial_numbers', 'phone_numbers'],
        'tax': ['tax_identifiers', 'percentages'],
        'account': ['account_numbers']
    }
    
    for keyword, keys in keyword_mapping.items():
        if keyword in prompt_lower:
            for key in keys:
                if key in data:
                    filtered[key] = data[key]
    
    return filtered if filtered else data

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
            vision_prompt = """Analyze this image/document comprehensively and extract ALL visible information including:
            
            TEXT CONTENT: All readable text, numbers, characters, headers, titles, labels
            FINANCIAL INFO: Monetary amounts, prices, totals, currency symbols, calculations
            CONTACT DATA: Names, addresses, phone numbers, emails, signatures
            BUSINESS INFO: Company names, logos, registration details, departments
            DOCUMENT DETAILS: Dates, timestamps, document numbers, references, IDs
            VISUAL ELEMENTS: Tables, charts, lists, stamps, seals, watermarks
            TECHNICAL DATA: Barcodes, QR codes, serial numbers, specifications
            
            Return comprehensive JSON with all extracted information organized by category."""
        else:
            vision_prompt = f"{sanitized_prompt}\n\nAnalyze the image thoroughly and extract the requested information accurately. Return results as JSON."

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
            return json.loads(result)
        except json.JSONDecodeError:
            return {"extracted_information": result}

    except Exception as e:
        return {"error": f"Image extraction failed: {str(e)}"}