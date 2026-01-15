from django.db import models

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('invoice', 'Invoice'),
        ('proforma', 'Proforma Invoice'),
        ('receipt', 'Receipt'),
        ('other', 'Other'),
    ]
    
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, blank=True)
    extracted_data = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.file.name} - {self.uploaded_at}"
