from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

EXTRACTION_PROMPT = """
Extract all relevant information from this document. The document could be an invoice, proforma invoice, receipt, or other business document.

Please extract the following information if available:
- Document type (invoice, proforma, receipt, etc.)
- Document number/ID
- Date
- Due date (if applicable)
- Vendor/Seller information (name, address, contact, tax ID)
- Customer/Buyer information (name, address, contact)
- Line items (description, quantity, unit price, total)
- Subtotal
- Tax amount and rate
- Total amount
- Currency
- Payment terms
- Bank details (if applicable)
- Any other relevant information

Return the data as a structured JSON object. If information is not available, omit the field or set it to null.
"""

def extract_info_from_text(text):
    """Extract information from text using OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a document parsing assistant that extracts structured information from business documents."},
                {"role": "user", "content": f"{EXTRACTION_PROMPT}\n\nDocument content:\n{text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": str(e)}

def extract_info_from_image(base64_image):
    """Extract information from image using OpenAI Vision"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": EXTRACTION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {"raw_response": content}
        
        return result
    except Exception as e:
        return {"error": str(e)}
