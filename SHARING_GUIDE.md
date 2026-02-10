# Sharing DocParse API with Users

## Steps to Share

### 1. Deploy to Render
Follow the instructions in `RENDER_DEPLOY.md` to deploy your API.

### 2. Update Postman Collection
After deployment, update the `base_url` in `DocParse_API.postman_collection.json`:

```json
"variable": [
  {
    "key": "base_url",
    "value": "https://your-actual-app-name.onrender.com",
    "type": "string"
  }
]
```

Replace `your-actual-app-name` with your Render app name.

### 3. Share with Users

**Option A: Share Postman Collection**
1. Send them the updated `DocParse_API.postman_collection.json` file
2. They import it into Postman: File → Import → Select the JSON file
3. They can immediately test all endpoints

**Option B: Share API Documentation**
Send them these URLs:
- **Swagger UI**: `https://your-app.onrender.com/swagger/`
- **ReDoc**: `https://your-app.onrender.com/redoc/`
- They can test the API directly in the browser

**Option C: Share cURL Examples**
```bash
# Extract all information (no prompt)
curl -X POST https://your-app.onrender.com/api/documents/ \
  -F "file=@invoice.pdf"

# Extract specific information (with prompt)
curl -X POST https://your-app.onrender.com/api/documents/ \
  -F "file=@invoice.pdf" \
  -F "prompt=What is the total amount?"
```

## What Users Need

**Nothing!** Your API is public and ready to use. Users just need:
- The API URL
- The Postman collection OR Swagger documentation
- Their documents to upload

## Important Notes

1. **No Authentication Required**: API is public (add auth if needed)
2. **Rate Limits**: 100 requests/hour for anonymous users
3. **File Size**: Check Render's upload limits
4. **Free Tier**: May spin down after 15 minutes of inactivity
5. **First Request**: May take 30-60 seconds after spin-down

## Example Usage for Users

### Using Postman
1. Import the collection
2. Select any request (e.g., "Extract All Information")
3. Click "Body" → Select file to upload
4. Click "Send"
5. View clean JSON response

### Using Swagger UI
1. Go to `https://your-app.onrender.com/swagger/`
2. Click on `/api/documents/` → "Try it out"
3. Upload file and optionally add prompt
4. Click "Execute"
5. View response

### Using Code (Python)
```python
import requests

url = "https://your-app.onrender.com/api/documents/"

with open("invoice.pdf", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},
        data={"prompt": "Extract all information"}
    )

print(response.json())
```

## Support

Users can refer to:
- **README.md**: Complete API documentation
- **Swagger UI**: Interactive API testing
- **Postman Collection**: Pre-configured requests with examples
