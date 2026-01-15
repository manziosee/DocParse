from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'document_type', 'processed', 'uploaded_at']
    list_filter = ['document_type', 'processed', 'uploaded_at']
    search_fields = ['file', 'document_type']
    readonly_fields = ['uploaded_at', 'extracted_data']
