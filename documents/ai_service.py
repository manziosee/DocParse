from django.conf import settings
import json
import re

def extract_custom_fields(text, custom_fields_str):
    """Extract specific fields requested by user"""
    if not custom_fields_str:
        return extract_info_from_text(text)  # Default extraction
    
    custom_fields = [field.strip().lower() for field in custom_fields_str.split(',')]
    result = {
        "custom_extraction": True,
        "requested_fields": custom_fields,
        "extracted_data": {}
    }
    
    text_lower = text.lower()
    
    for field in custom_fields:
        if field in ['items', 'line_items', 'products']:
            # Extract line items
            item_patterns = [
                r'(\d+)\s*([A-Za-z][A-Za-z\s]+?)\s+(\d+)\s+([\d,]+)\s+([\d,]+)',
                r'([A-Za-z][A-Za-z\s]+Chair|[A-Za-z][A-Za-z\s]+Desk|[A-Za-z][A-Za-z\s]+Shelf|[A-Za-z][A-Za-z\s]+Lamp)',
                r'(?:chair|desk|shelf|lamp|cabinet|table)\s*[A-Za-z\s]*',
            ]
            items_found = []
            for pattern in item_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    if isinstance(matches[0], tuple) and len(matches[0]) >= 2:
                        # Full line item match
                        for match in matches:
                            items_found.append(match[1].strip())
                    else:
                        # Simple item name match
                        items_found.extend([m.strip() for m in matches if len(m.strip()) > 2])
                    break
            
            if items_found:
                result["extracted_data"][field] = ", ".join(items_found[:5])  # First 5 items
            else:
                # Fallback: look for common item words
                item_words = re.findall(r'\b(chair|desk|shelf|lamp|cabinet|table|bookshelf)\b', text, re.IGNORECASE)
                if item_words:
                    result["extracted_data"][field] = ", ".join(set(item_words))
        
        elif field in ['name', 'company_name', 'vendor_name', 'customer_name']:
            # Extract names (first few lines or after "to:")
            name_patterns = [
                r'(?:company|vendor|from|bill\s+from)[:\s]+([A-Za-z\s&.,]+)',
                r'(?:to|customer|client)[:\s]+([A-Za-z\s&.,]+)',
                r'^([A-Za-z\s&.,]{3,30})$'  # Standalone names
            ]
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    result["extracted_data"][field] = match.group(1).strip()
                    break
        
        elif field in ['amount', 'total', 'price', 'cost', 'sum']:
            # Extract amounts - improved patterns
            amount_patterns = [
                rf'total[:\s]*(?:rwf)?\s*([\d,]+)',  # Total: RWF 654,900
                rf'subtotal[:\s]*(?:rwf)?\s*([\d,]+)',  # Subtotal: RWF 555,000
                rf'{field}[:\s]*(?:rwf|usd|eur|\$)?\s*([\d,]+\.?\d*)',
                r'(?:total|amount|sum|price)[:\s]*(?:rwf|usd|eur|\$)?\s*([\d,]+\.?\d*)',
                r'(?:rwf|usd|eur|\$)\s*([\d,]+\.?\d*)',
                r'([\d,]+\.\d{2})'
            ]
            for pattern in amount_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["extracted_data"][field] = match.group(1).replace(',', '')
                    break
        
        elif field in ['code', 'purchase_code', 'order_code', 'reference', 'ref', 'id']:
            # Extract codes/references
            code_patterns = [
                rf'{field}[:\s#]*([A-Z0-9-]+)',
                r'(?:ref|reference|code|id|order)[:\s#]*([A-Z0-9-]+)',
                r'#([A-Z0-9-]+)',
                r'([A-Z]{2,}-\d{4}-\d+)'
            ]
            for pattern in code_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["extracted_data"][field] = match.group(1)
                    break
        
        elif field in ['phone', 'telephone', 'mobile']:
            # Extract phone numbers
            phone_patterns = [
                r'(?:phone|tel|mobile)[:\s]*([\d\s\-\+\(\)]{10,})',
                r'([\+]?[\d\s\-\(\)]{10,})',
            ]
            for pattern in phone_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["extracted_data"][field] = match.group(1).strip()
                    break
        
        elif field in ['email', 'mail']:
            # Extract email addresses
            email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            match = re.search(email_pattern, text)
            if match:
                result["extracted_data"][field] = match.group(1)
        
        elif field in ['date', 'invoice_date', 'order_date']:
            # Extract dates
            date_patterns = [
                rf'{field}[:\s]*([\d]{{4}}-[\d]{{2}}-[\d]{{2}}|[\d]{{2}}[-/][\d]{{2}}[-/][\d]{{4}})',
                r'date[:\s]*([\d]{4}-[\d]{2}-[\d]{2}|[\d]{2}[-/][\d]{2}[-/][\d]{4})',
                r'([\d]{4}-[\d]{2}-[\d]{2})',
                r'([\d]{2}[-/][\d]{2}[-/][\d]{4})'
            ]
            for pattern in date_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["extracted_data"][field] = match.group(1)
                    break
        
        elif field in ['address', 'location']:
            # Extract addresses (lines with street/city patterns)
            address_patterns = [
                r'(?:address|location)[:\s]+([A-Za-z0-9\s,.-]+(?:street|road|avenue|drive|blvd)[A-Za-z0-9\s,.-]*)',
                r'([A-Za-z0-9\s,.-]*(?:street|road|avenue|drive|blvd)[A-Za-z0-9\s,.-]*)',
                r'([A-Za-z\s,]+,\s*[A-Za-z\s]+)'
            ]
            for pattern in address_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["extracted_data"][field] = match.group(1).strip()
                    break
        
        else:
            # Generic field extraction
            generic_pattern = rf'{field}[:\s]+([A-Za-z0-9\s.-]+)'
            match = re.search(generic_pattern, text, re.IGNORECASE)
            if match:
                result["extracted_data"][field] = match.group(1).strip()
    
    result["extraction_method"] = "Custom Field Extraction (Free)"
    result["note"] = f"Extracted {len(result['extracted_data'])} of {len(custom_fields)} requested fields"
    
    return result

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
