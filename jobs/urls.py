from django.urls import path
from .views import JobViewSet

urlpatterns = [
    
    path('', JobViewSet.as_view({'get': 'list', 'post': 'create'}), name='job-list'),
    path('<int:pk>/', JobViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='job-detail'),
    path('company/<int:company_id>/', JobViewSet.as_view({'get': 'list_by_company'}), name='job-list-by-company'),
  
]