from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organizations.models import Organization
import logging

class OrganizationGetView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request):
    subdomain = request.headers.get('x-subdomain')

    if not subdomain:
      return Response({'detail': 'サブドメインが送信されていません'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      organization = Organization.objects.get(sub_domain=subdomain)
    except Organization.DoesNotExist:
      return Response({'detail': '組織が存在しません'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
      'name': organization.name,
      'logo': request.build_absolute_uri(organization.logo.url) if organization.logo else None
    })
