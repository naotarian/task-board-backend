from django.urls import path
from .views import VerifyEmailView
from users.auth_views.resend_verification_email_view import ResendVerificationEmailView
from users.auth_views.login_view import LoginView
from users.auth_views.logout_view import LogoutView
from users.auth_views.password_reset_view import PasswordResetView, PasswordResetConfirmView
from users.auth_views.register_view import RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationEmailView.as_view()),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
