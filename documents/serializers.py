from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Natural language prompt describing what information to extract (e.g., 'Extract all contact information and amounts' or 'Get vendor details and line items')"
    )
    
    class Meta:
        model = Document
        fields = ['id', 'file', 'document_type', 'prompt', 'extracted_data', 'uploaded_at', 'processed']
        read_only_fields = ['extracted_data', 'uploaded_at', 'processed']
    
    def create(self, validated_data):
        # Remove prompt from validated_data as it's not a model field
        prompt = validated_data.pop('prompt', '')
        document = super().create(validated_data)
        # Store prompt in the document instance for processing
        document._prompt = prompt
        return document
