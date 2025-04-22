from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from .models.project import Project
from .models.member import ProjectMember
from .models.member_role import ProjectMemberRole
from projects.models.role import Role
from django.db import transaction

class ProjectCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    data = request.data.copy()
    serializer = ProjectSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
      with transaction.atomic():
        # ① プロジェクトを保存（画像は後で）
        project = Project.objects.create(
          name=data["name"],
          description=data.get("description", ""),
          owner=request.user,
        )

        # ② サムネイルがあれば保存
        if "thumbnail" in request.FILES:
          project.thumbnail = request.FILES["thumbnail"]
          project.save()

        # ③ 作成者をメンバーとして登録
        member = ProjectMember.objects.create(
          project=project,
          user=request.user,
        )

        # ④ ロールを取得（owner）
        owner_role = Role.objects.get(name="owner")

        # ⑤ メンバーロールを登録
        ProjectMemberRole.objects.create(
          member=member,
          role=owner_role,
        )

    except Role.DoesNotExist:
      return Response(
        {"detail": "ロール 'owner' が見つかりません"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
      )
    except Exception as e:
      return Response(
          {"detail": f"エラーが発生しました: {str(e)}"},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

    return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

class ProjectDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, pk):
    project = get_object_or_404(Project, pk=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

class ProjectListView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    projects = Project.objects.filter(owner=request.user).order_by("-created_at")
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
