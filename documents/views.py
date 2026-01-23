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
    API endpoint for document upload and information extraction.
    
    Supports PDF, Word (.docx), and image files (JPG, PNG, etc.).
    Uses AI to extract information based on user prompts.
    """
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer
    
    @swagger_auto_schema(
        operation_summary="Upload Document",
        operation_description="Upload a document (PDF, Word, or Image) and extract information using AI based on your natural language prompt",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Document file (PDF, DOCX, JPG, PNG, etc.)'
                ),
                'prompt': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Natural language prompt describing what information to extract (e.g., "Extract all contact information and amounts")',
                    example='Extract vendor name, total amount, and all line items'
                ),
                'document_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Optional document type classification',
                    enum=['invoice', 'proforma', 'receipt', 'other'],
                    example='invoice'
                )
            },
            required=['file']
        ),
        responses={
            201: openapi.Response(
                'Document uploaded and processed successfully',
                DocumentSerializer,
                examples={
                    'application/json': {
                        'id': 1,
                        'file': '/media/documents/invoice.pdf',
                        'document_type': 'invoice',
                        'extracted_data': {
                            'vendor_name': 'ABC Company Inc.',
                            'total_amount': '$1,250.00',
                            'line_items': [
                                {
                                    'description': 'Web Development Services',
                                    'quantity': 40,
                                    'unit_price': '$25.00',
                                    'total': '$1,000.00'
                                }
                            ]
                        },
                        'uploaded_at': '2024-01-15T10:30:00Z',
                        'processed': True
                    }
                }
            ),
            400: openapi.Response('Bad Request - Invalid file or data'),
        },
        consumes=['multipart/form-data']
    )
    def create(self, request, *args, **kwargs):
        """Upload and process document with custom prompt"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        # Process the document
        try:
            file_path = document.file.path
            filename = document.file.name
            
            # Extract content based on file type
            content, content_type = process_document(file_path, filename)
            
            # Get user prompt
            prompt = getattr(document, '_prompt', '')
            
            # Extract information using AI with user prompt
            if content_type == 'text':
                if prompt.strip():
                    extracted_data = extract_info_with_prompt(content, prompt)
                else:
                    extracted_data = extract_info_from_text(content)
            else:  # image
                extracted_data = extract_info_from_image(content)
            
            # Update document with extracted data
            document.extracted_data = extracted_data
            document.processed = True
            
            # Auto-detect document type if not provided
            if not document.document_type and isinstance(extracted_data, dict) and 'document_type' in extracted_data:
                doc_type = str(extracted_data['document_type']).lower()
                if 'proforma' in doc_type:
                    document.document_type = 'proforma'
                elif 'invoice' in doc_type:
                    document.document_type = 'invoice'
                elif 'receipt' in doc_type:
                    document.document_type = 'receipt'
                else:
                    document.document_type = 'other'
            
            document.save()
            
        except Exception as e:
            document.extracted_data = {"error": str(e)}
            document.processed = True
            document.save()
        
        return Response(
            self.get_serializer(document).data,
            status=status.HTTP_201_CREATED
        )
    
    @swagger_auto_schema(
        operation_summary="List Documents",
        operation_description="Retrieve a list of all uploaded documents with their extracted data",
        responses={
            200: openapi.Response(
                'List of documents retrieved successfully',
                DocumentSerializer(many=True),
                examples={
                    'application/json': [
                        {
                            'id': 1,
                            'file': '/media/documents/invoice.pdf',
                            'document_type': 'invoice',
                            'extracted_data': {
                                'vendor_name': 'ABC Company',
                                'total_amount': '$120.00'
                            },
                            'uploaded_at': '2024-01-15T10:30:00Z',
                            'processed': True
                        }
                    ]
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """List all documents"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
