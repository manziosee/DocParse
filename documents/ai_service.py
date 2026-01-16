from django.conf import settings
import json
import re

def extract_info_from_text(text):
    """Extract and organize information from text"""
    try:
        result = {
            "document_info": {},
            "vendor": {},
            "customer": {},
            "line_items": [],
            "financial_summary": {},
            "additional_info": {}
        }
        
        text_lower = text.lower()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # === DOCUMENT INFO ===
        if "proforma" in text_lower:
            result["document_info"]["type"] = "Proforma Invoice"
        elif "invoice" in text_lower:
            result["document_info"]["type"] = "Invoice"
        elif "receipt" in text_lower:
            result["document_info"]["type"] = "Receipt"
        else:
            result["document_info"]["type"] = "Other"
        
        # Document number
        doc_num = re.search(r'(?:invoice|pro|receipt|ref|#)[\s#:]*([A-Z0-9-]+)', text, re.IGNORECASE)
        if doc_num:
            result["document_info"]["number"] = doc_num.group(1)
        
        # Date
        date_match = re.search(r'date[:\s]*([\d]{4}-[\d]{2}-[\d]{2}|[\d]{2}[-/][\d]{2}[-/][\d]{4})', text, re.IGNORECASE)
        if date_match:
            result["document_info"]["date"] = date_match.group(1)
        
        # === VENDOR INFO ===
        vendor_lines = []
        for i, line in enumerate(lines[:15]):
            if any(x in line.lower() for x in ['date:', 'invoice', 'bill to']):
                break
            if line and len(line) > 2:
                vendor_lines.append(line)
        
        if vendor_lines:
            result["vendor"]["name"] = vendor_lines[0]
            if len(vendor_lines) > 1:
                result["vendor"]["address"] = ", ".join(vendor_lines[1:4])
        
        # === CUSTOMER INFO ===
        bill_to = re.search(r'bill\s+to[:\s]*(.*?)(?=items|#|subtotal|total|$)', text, re.IGNORECASE | re.DOTALL)
        if bill_to:
            customer_lines = [l.strip() for l in bill_to.group(1).split('\n') if l.strip() and len(l.strip()) > 2]
            if customer_lines:
                result["customer"]["name"] = customer_lines[0]
                if len(customer_lines) > 1:
                    result["customer"]["address"] = ", ".join(customer_lines[1:4])
        
        # === LINE ITEMS ===
        item_matches = re.findall(
            r'(\d+)\s+([A-Za-z][A-Za-z\s]+?)\s+(\d+)\s+([\d,]+)\s+([\d,]+)',
            text
        )
        
        for match in item_matches:
            result["line_items"].append({
                "#": match[0],
                "description": match[1].strip(),
                "quantity": int(match[2]),
                "unit_price": match[3].replace(',', ''),
                "total": match[4].replace(',', '')
            })
        
        # === FINANCIAL SUMMARY ===
        subtotal = re.search(r'subtotal[:\s]*(?:rwf|usd|eur)?\s*([\d,]+)', text, re.IGNORECASE)
        if subtotal:
            result["financial_summary"]["subtotal"] = subtotal.group(1).replace(',', '')
        
        tax = re.search(r'tax[\s\(]*([\d]+)%?[\)]*[:\s]*(?:rwf|usd|eur)?\s*([\d,]+)', text, re.IGNORECASE)
        if tax:
            result["financial_summary"]["tax_rate"] = tax.group(1) + "%"
            result["financial_summary"]["tax_amount"] = tax.group(2).replace(',', '')
        
        total = re.search(r'(?:^|\n)\s*total[:\s]*(?:rwf|usd|eur)?\s*([\d,]+)', text, re.IGNORECASE | re.MULTILINE)
        if total:
            result["financial_summary"]["total"] = total.group(1).replace(',', '')
        
        # Currency
        currency = re.search(r'\b(RWF|USD|EUR|GBP|JPY|CNY)\b', text, re.IGNORECASE)
        if currency:
            result["financial_summary"]["currency"] = currency.group(1).upper()
        
        # === ADDITIONAL INFO ===
        result["additional_info"]["extraction_method"] = "Pattern Matching (Free)"
        result["additional_info"]["total_items"] = len(result["line_items"])
        result["additional_info"]["note"] = "For AI-powered extraction with higher accuracy, add OpenAI credits"
        
        # Clean up empty sections
        result = {k: v for k, v in result.items() if v}
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "note": "Extraction failed. Please check document format."
        }

def extract_info_from_image(base64_image):
    """Extract information from image"""
    return {
        "document_info": {
            "type": "Image Document",
            "status": "Uploaded successfully"
        },
        "additional_info": {
            "extraction_method": "Basic (Free)",
            "note": "Image received. For OCR and AI extraction, add OpenAI credits or the image will be processed as text if OCR is available."
        }
    }
