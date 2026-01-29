from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    path('documents/', DocumentViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='document-list'),
]
