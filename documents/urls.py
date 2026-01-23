from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

# Custom URL patterns for specific actions only
urlpatterns = [
    path('documents/', DocumentViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='document-list'),
]
