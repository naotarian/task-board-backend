from django.urls import path
from organizations.views.organization_create_view import OrganizationCreateView

urlpatterns = [
  path("create/", OrganizationCreateView.as_view(), name="organization-create"),
]
