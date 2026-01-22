from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    custom_fields = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Comma-separated list of fields to extract (e.g., 'name,amount,purchase_code,phone,email')"
    )
    
    class Meta:
        model = Document
        fields = ['id', 'file', 'document_type', 'custom_fields', 'extracted_data', 'uploaded_at', 'processed']
        read_only_fields = ['extracted_data', 'uploaded_at', 'processed']
    
    def create(self, validated_data):
        # Remove custom_fields from validated_data as it's not a model field
        custom_fields = validated_data.pop('custom_fields', '')
        document = super().create(validated_data)
        # Store custom_fields in the document instance for processing
        document._custom_fields = custom_fields
        return document
