from django.urls import path
from .views import UserRegistrationView, VerifyEmail

urlpatterns = [
    # Example URL patterns
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path("register/", UserRegistrationView.as_view(), name="register"),
    # path('profile/', views.profile_view, name='profile'),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
]
