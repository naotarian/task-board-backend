from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from organizations.models import OrganizationUser
from rest_framework import status
import logging

class UserOrganizationsView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    logger = logging.getLogger('development')
    logger.info(f'[UserOrganizations] ログインユーザー: {user}')

    organizations = OrganizationUser.objects.select_related('organization').filter(
      user=user,
      deleted_at__isnull=True,
      organization__deleted_at__isnull=True
    )

    data = [
      {
        'id': ou.organization.id,
        'name': ou.organization.name,
        'subdomain': ou.organization.sub_domain,
        'thumbnail': ou.organization.logo.url if ou.organization.logo else None,
      }
      for ou in organizations
    ]

    return Response(data, status=status.HTTP_200_OK)
