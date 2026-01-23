import openai
import re
from typing import Dict, Any
from django.conf import settings

def extract_info_with_prompt(content: str, prompt: str = "") -> Dict[str, Any]:
    """
    Extract information from document content based on user prompt using OpenAI.
    """
    if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
        return {"error": "OpenAI API key not configured. Please set OPENAI_API_KEY in environment."}
    
    try:
        openai.api_key = settings.OPENAI_API_KEY
        
        # Default prompt if none provided
        if not prompt.strip():
            prompt = "Extract all relevant information from this document including names, amounts, dates, contact information, and any other important details."
        
        # Create the extraction prompt
        extraction_prompt = f"""
        You are a document information extraction expert. 
        
        User Request: {prompt}
        
        Document Content:
        {content[:4000]}  # Limit content to avoid token limits
        
        Please extract the requested information and return it as a JSON object. 
        Be specific and accurate. If information is not found, don't make it up.
        """
        
        response = openai.ChatCompletion.create(
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
        except:
            return {"extracted_information": result}
            
    except Exception as e:
        return {"error": f"OpenAI extraction failed: {str(e)}"}

def extract_info_from_text(content: str) -> Dict[str, Any]:
    """
    Fallback extraction using OpenAI with default comprehensive prompt.
    """
    return extract_info_with_prompt(content, "Extract all important information from this document including financial details, contact information, dates, and document metadata.")

def extract_info_from_image(image_path: str) -> Dict[str, Any]:
    """
    Extract information from image using OpenAI Vision API.
    """
    if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
        return {"error": "OpenAI API key not configured"}
    
    try:
        import base64
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        openai.api_key = settings.OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
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
        except:
            return {"extracted_information": result}
            
    except Exception as e:
        return {"error": f"Image extraction failed: {str(e)}"}