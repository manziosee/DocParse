from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    path('documents/', DocumentViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='document-list'),
    path('documents/<int:pk>/', DocumentViewSet.as_view({
        'get': 'retrieve'
    }), name='document-detail'),
    path('documents/<int:pk>/extract/', DocumentViewSet.as_view({
        'post': 'extract'
    }), name='document-extract'),
]
