from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Document
from .serializers import DocumentSerializer
from .utils import process_document
from .ai_service import extract_info_from_text, extract_info_from_image
import os

class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for document upload and information extraction.
    
    Supports PDF, Word (.docx), and image files (JPG, PNG, etc.).
    Uses AI to extract structured information from invoices, proforma invoices, receipts, and other documents.
    """
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer
    
    @swagger_auto_schema(
        operation_description="Upload a document (PDF, Word, or Image) and extract information using AI",
        responses={
            201: openapi.Response('Document uploaded and processed successfully', DocumentSerializer),
            400: 'Bad Request - Invalid file or data',
        }
    )
    def create(self, request, *args, **kwargs):
        """Upload and process document"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        # Process the document
        try:
            file_path = document.file.path
            filename = document.file.name
            
            # Extract content based on file type
            content, content_type = process_document(file_path, filename)
            
            # Extract information using AI
            if content_type == 'text':
                extracted_data = extract_info_from_text(content)
            else:  # image
                extracted_data = extract_info_from_image(content)
            
            # Update document with extracted data
            document.extracted_data = extracted_data
            document.processed = True
            
            # Auto-detect document type if not provided
            if not document.document_type and 'document_type' in extracted_data:
                doc_type = extracted_data['document_type'].lower()
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
        operation_description="Reprocess an existing document to extract information again",
        responses={
            200: openapi.Response('Document reprocessed successfully', DocumentSerializer),
            404: 'Document not found',
            500: 'Internal server error during processing',
        }
    )
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """Reprocess a document"""
        document = self.get_object()
        
        try:
            file_path = document.file.path
            filename = document.file.name
            
            content, content_type = process_document(file_path, filename)
            
            if content_type == 'text':
                extracted_data = extract_info_from_text(content)
            else:
                extracted_data = extract_info_from_image(content)
            
            document.extracted_data = extracted_data
            document.processed = True
            document.save()
            
            return Response(self.get_serializer(document).data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
