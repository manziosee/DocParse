from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DocParse API - ChatGPT Style - SMART IT CONSULTING",
        default_version='v1',
        description="""AI-Powered Document Parser API that works like ChatGPT!
        
        **🚀 How it works:**
        1. **Upload** any document (PDF, Word, Image)
        2. **Chat** with your document using natural language
        3. **Ask unlimited questions** about the same document
        
        **💬 ChatGPT-Style Interaction:**
        - Upload once, ask unlimited questions
        - Natural language prompts like "What is the vendor name?"
        - Get structured JSON responses
        - Works with any document type
        
        **📄 Supported Formats:**
        - PDF files (.pdf)
        - Word documents (.docx, .doc)
        - Images (.jpg, .png, .gif, etc.)
        
        **🎯 Example Questions:**
        - "What is the vendor name and total amount?"
        - "List all line items with prices"
        - "What are the payment terms?"
        - "Give me all contact information"
        - "What are the key dates in this document?"
        
        **🔧 Usage:**
        1. POST /api/documents/ - Upload your document
        2. POST /api/documents/{id}/extract/ - Ask questions about it
        
        Built by SMART IT CONSULTING - 2025
        """,
        contact=openapi.Contact(
            name="SMART IT CONSULTING",
            email="manziosee3@gmail.com"
        ),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('documents.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
