from django.conf import settings
from django.http import JsonResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_info_with_prompt(content: str, prompt: str = "") -> dict:
    """
    Extract information from document content based on user prompt using OpenAI.
    """
    try:
        # Check if OpenAI is available
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured")
            return {"error": "OpenAI API key not configured. Please set OPENAI_API_KEY in environment."}
        
        # Try importing OpenAI
        try:
            from openai import OpenAI
        except ImportError:
            logger.error("OpenAI library not installed")
            return {"error": "OpenAI library not available"}
        
        # Default prompt if none provided
        if not prompt.strip():
            prompt = "Extract all relevant information from this document including names, amounts, dates, contact information, and any other important details."
        
        # Create the extraction prompt
        extraction_prompt = f"""
        You are a document information extraction expert. 
        
        User Request: {prompt}
        
        Document Content:
        {content[:4000]}
        
        Please extract the requested information and return it as a JSON object. 
        Be specific and accurate. If information is not found, don't make it up.
        """
        
        # Use the new OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert document parser. Extract information as requested and return valid JSON."},
                {"role": "user", "content": extraction_prompt}
            ],
            max_tokens=1500,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
        # Try to parse as JSON, if it fails return as text
        try:
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            return {"extracted_information": result}
            
    except Exception as e:
        logger.error(f"OpenAI extraction failed: {str(e)}")
        return {"error": f"OpenAI extraction failed: {str(e)}"}

def extract_info_from_text(content: str) -> dict:
    """
    Fallback extraction using OpenAI with default comprehensive prompt.
    """
    return extract_info_with_prompt(content, "Extract all important information from this document including financial details, contact information, dates, and document metadata.")

def extract_info_from_image(image_path: str) -> dict:
    """
    Extract information from image using OpenAI Vision API.
    """
    try:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return {"error": "OpenAI API key not configured"}
        
        import base64
        from openai import OpenAI
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all information from this document image. Return the data as JSON."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1500
        )
        
        result = response.choices[0].message.content.strip()
        
        try:
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            return {"extracted_information": result}
            
    except Exception as e:
        logger.error(f"Image extraction failed: {str(e)}")
        return {"error": f"Image extraction failed: {str(e)}"}