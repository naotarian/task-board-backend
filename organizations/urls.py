from django.urls import path
from organizations.views.organization_create_view import OrganizationCreateView
from organizations.views.organization_get_view import OrganizationGetView
from .views.subdomain import check_subdomain

urlpatterns = [
  path("", OrganizationGetView.as_view(), name="organization-get"),
  path("create/", OrganizationCreateView.as_view(), name="organization-create"),
  path('check-subdomain/', check_subdomain, name='check_subdomain'),
]
