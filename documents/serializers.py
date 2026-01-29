from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'document_type', 'extracted_data', 'uploaded_at', 'processed']
        read_only_fields = ['extracted_data', 'uploaded_at', 'processed']
