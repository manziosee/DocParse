from rest_framework import viewsets, status
from rest_framework.decorators import action
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
        operation_description="Upload a document (PDF, Word, or Image) for processing. Document will be stored and ready for extraction queries.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Document file (PDF, DOCX, JPG, PNG, etc.)'
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
                'Document uploaded successfully',
                DocumentSerializer,
                examples={
                    'application/json': {
                        'id': 1,
                        'file': '/media/documents/invoice.pdf',
                        'document_type': 'invoice',
                        'extracted_data': {},
                        'uploaded_at': '2024-01-15T10:30:00Z',
                        'processed': False
                    }
                }
            ),
            400: openapi.Response('Bad Request - Invalid file or data'),
        },
        consumes=['multipart/form-data']
    )
    def create(self, request, *args, **kwargs):
        """Upload document for processing"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        return Response(
            self.get_serializer(document).data,
            status=status.HTTP_201_CREATED
        )
    
    @swagger_auto_schema(
        operation_summary="Extract Information",
        operation_description="Send a natural language prompt to extract specific information from an uploaded document. Works like ChatGPT - ask anything about the document!",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'prompt': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Natural language prompt describing what to extract',
                    example='What is the vendor name and total amount?'
                )
            },
            required=['prompt']
        ),
        responses={
            200: openapi.Response(
                'Information extracted successfully',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'prompt': openapi.Schema(type=openapi.TYPE_STRING),
                        'response': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'document_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                ),
                examples={
                    'application/json': {
                        'prompt': 'What is the vendor name and total amount?',
                        'response': {
                            'vendor_name': 'ABC Company Inc.',
                            'total_amount': '$1,250.00'
                        },
                        'document_id': 1
                    }
                }
            ),
            404: openapi.Response('Document not found'),
        }
    )
    @action(detail=True, methods=['post'])
    def extract(self, request, pk=None):
        """Extract information using natural language prompt"""
        document = self.get_object()
        prompt = request.data.get('prompt', '')
        
        if not prompt.strip():
            return Response(
                {'error': 'Prompt is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
                'response': extracted_data,
                'document_id': document.id
            })
            
        except Exception as e:
            import logging
            logging.error(f"Extraction failed: {str(e)}")
            return Response(
                {'error': 'Extraction failed'},
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
    
    @swagger_auto_schema(
        operation_summary="Get Document Details",
        operation_description="Retrieve details of a specific document",
        responses={
            200: openapi.Response('Document details', DocumentSerializer),
            404: openapi.Response('Document not found')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Get document details"""
        document = self.get_object()
        serializer = self.get_serializer(document)
        return Response(serializer.data)
