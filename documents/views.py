from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Document
from .serializers import DocumentSerializer
from .utils import process_document
from .ai_service import extract_info_with_prompt, extract_info_from_image
import os

class DocumentViewSet(viewsets.GenericViewSet):
    """
    API endpoint for document upload and immediate information extraction.
    
    Upload any document (PDF, Word, Image) with a prompt and get instant results.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    @swagger_auto_schema(
        operation_summary="Upload Document and Extract Information",
        operation_description="Upload a document and extract information. Provide a prompt to extract specific information, or leave empty to extract all information from the document.",
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="Document file (PDF, DOCX, JPG, PNG, TXT, etc.)",
                type=openapi.TYPE_FILE,
                required=True
            ),
            openapi.Parameter(
                'prompt',
                openapi.IN_FORM,
                description="Optional: Natural language prompt describing what to extract. If empty, extracts all information.",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'document_type',
                openapi.IN_FORM,
                description="Optional document type classification",
                type=openapi.TYPE_STRING,
                enum=['invoice', 'proforma', 'receipt', 'other'],
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                'Information extracted successfully',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_amount': openapi.Schema(type=openapi.TYPE_STRING, example='RWF 654,900'),
                        'names': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'dates': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'companies': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                    }
                )
            ),
            400: openapi.Response('Bad Request - Invalid file'),
        },
        consumes=['multipart/form-data']
    )
    def create(self, request, *args, **kwargs):
        """Upload document and extract information with prompt"""
        prompt = request.data.get('prompt', '')
        
        # Prompt is optional - if empty, extract all information
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        # Process the document immediately
        try:
            file_path = document.file.path
            filename = document.file.name
            
            # Extract content based on file type
            content, content_type = process_document(file_path, filename)
            
            # Extract information using user prompt
            if content_type == 'text':
                extracted_data = extract_info_with_prompt(content, prompt)
            else:  # image
                extracted_data = extract_info_from_image(file_path, prompt)
            
            # Return only the extracted data, no metadata
            return Response(extracted_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import logging
            logging.error(f"Document processing failed: {str(e)}")
            return Response(
                {'error': f'Document processing failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )