from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({
        "status": "healthy",
        "service": "DocParse API",
        "version": "1.0.0"
    })

schema_view = get_schema_view(
    openapi.Info(
        title="DocParse API - SMART IT CONSULTING",
        default_version='v1',
        description="""AI-Powered Document Parser API - Upload and Extract!
        
        **How it works:**
        1. Upload any document (PDF, Word, Text, Image)
        2. Optionally ask a question about it in natural language
        3. Get instant AI-powered answers
        
        **Simple as that!**
        - No complex workflows
        - Single endpoint
        - Just upload and optionally ask
        
        **Supported Formats:**
        PDF, Word (.docx), Text (.txt), Images (JPG, PNG, etc.)
        
        **Example Usage:**
        - With prompt: "What is the total amount?"
        - Without prompt: Extracts all information automatically
        
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
    path('', health_check, name='health'),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/', include('documents.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
