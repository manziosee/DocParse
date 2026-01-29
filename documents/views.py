from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Document
from .serializers import DocumentSerializer
from .utils import process_document
from .ai_service import extract_info_from_text, extract_info_from_image, extract_info_with_prompt
import os

class DocumentViewSet(viewsets.GenericViewSet):
    """
    API endpoint for document upload and immediate information extraction.
    
    Upload any document (PDF, Word, Image) with a prompt and get instant results.
    No need to manage document IDs - just upload and ask!
    """
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer
    
    @swagger_auto_schema(
        operation_summary="Upload Document and Extract Information",
        operation_description="Upload a document and immediately extract information using a natural language prompt. No need to deal with document IDs!",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Document file (PDF, DOCX, JPG, PNG, etc.)'
                ),
                'prompt': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Natural language prompt describing what to extract',
                    example='List all the line items with their quantities and prices'
                ),
                'document_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Optional document type classification',
                    enum=['invoice', 'proforma', 'receipt', 'other'],
                    example='invoice'
                )
            },
            required=['file', 'prompt']
        ),
        responses={
            201: openapi.Response(
                'Document processed and information extracted successfully',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'prompt': openapi.Schema(type=openapi.TYPE_STRING),
                        'response': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                ),
                examples={
                    'application/json': {
                        'prompt': 'List all the line items with their quantities and prices',
                        'response': {
                            'line_items': [
                                {
                                    'item': 'Office Chair',
                                    'quantity': 2,
                                    'unit_price': 'RWF 75,000',
                                    'total': 'RWF 150,000'
                                }
                            ]
                        }
                    }
                }
            ),
            400: openapi.Response('Bad Request - Invalid file or missing prompt'),
        },
        consumes=['multipart/form-data']
    )
    def create(self, request, *args, **kwargs):
        """Upload document and immediately extract information with prompt"""
        prompt = request.data.get('prompt', '')
        
        if not prompt.strip():
            return Response(
                {'error': 'Prompt is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        # Process the document immediately
        try:
            file_path = document.file.path
            filename = document.file.name
            
            # Extract content based on file type
            content, content_type = process_document(file_path, filename)
            
            # Extract information using AI with user prompt
            if content_type == 'text':
                extracted_data = extract_info_with_prompt(content, prompt)
            else:  # image
                extracted_data = extract_info_from_image(content)
            
            return Response({
                'prompt': prompt,
                'response': extracted_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import logging
            logging.error(f"Document processing failed: {str(e)}")
            return Response(
                {'error': 'Document processing failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_summary="List Documents",
        operation_description="Retrieve a list of all uploaded documents",
        responses={
            200: openapi.Response(
                'List of documents retrieved successfully',
                DocumentSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """List all documents"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
