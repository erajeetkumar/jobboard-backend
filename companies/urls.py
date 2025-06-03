from django.urls import path

from .views import (
    CompanyPublicDetail,
    CompanyInternalDetail,
    CompanyListCreateView,
    CompanyMemberListCreateView,
    CompanyMemberUpdateDeleteView
)

urlpatterns = [
    
    path('', CompanyListCreateView.as_view(), name='company-list-create'),
    
    # Public
    path('<slug:slug>/', CompanyPublicDetail.as_view(), name='company-public-detail'),

    # Internal (authenticated)    
    path('id/<int:pk>/', CompanyInternalDetail.as_view(), name='company-internal-detail'),

    # Member management
    #path('<int:pk>/members/', CompanyMemberListCreateView.as_view(), name='company-members'),
    #path('<int:pk>/members/<int:user_id>/', CompanyMemberUpdateDeleteView.as_view(), name='company-member-detail'),
]