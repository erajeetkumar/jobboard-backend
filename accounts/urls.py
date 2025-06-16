from django.urls import path
from .views import UserRegistrationView, VerifyEmail, ResendVerificationEmailView

urlpatterns = [
    # Example URL patterns
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
    #resend verification email
    path("resend-verification-email/", ResendVerificationEmailView.as_view(), name="resend-verification-email"),
]
