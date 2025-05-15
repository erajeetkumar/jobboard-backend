from django.urls import path
from .views import CompanyViewSet

urlpatterns = [
    
    path('', CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
    path('<int:pk>/', CompanyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='company-detail'),
  
]