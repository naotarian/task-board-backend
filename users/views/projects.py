from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


from projects.models import ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProjectListView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    subdomain = request.headers.get("x-subdomain")

    project_memberships = (
      ProjectMember.objects
      .select_related("project", "project__organization")
      .filter(
        user=user,
        deleted_at__isnull=True,
        project__deleted_at__isnull=True
      )
    )

    # サブドメインが指定されていたら、その組織のみに絞る
    if subdomain:
      project_memberships = project_memberships.filter(
        project__organization__sub_domain=subdomain
      )

    projects_data = [
      {
        "id": pm.project.id,
        "name": pm.project.name,
        "thumbnail": pm.project.thumbnail.url if pm.project.thumbnail else None,
        "organization": {
          "id": pm.project.organization.id,
          "name": pm.project.organization.name,
          "subdomain": pm.project.organization.sub_domain,
        }
      }
      for pm in project_memberships
    ]

    return Response(projects_data)
