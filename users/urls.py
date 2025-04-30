from django.urls import path
from users.views.resend_verification_email_view import ResendVerificationEmailView
from users.views.login_view import LoginView
from users.views.logout_view import LogoutView
from users.views.password_reset_view import PasswordResetView, PasswordResetConfirmView
from users.views.register_view import RegisterView
from users.views.organizations import UserOrganizationsView
from users.views.me import MeView
from users.views.verify_email import VerifyEmailView
from users.views.projects import UserProjectListView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationEmailView.as_view()),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('user/organizations/', UserOrganizationsView.as_view(), name='user-organizations'),
    path('user/projects/', UserProjectListView.as_view(), name='me-projects'),
    path('me/', MeView.as_view(), name='me'),
]
