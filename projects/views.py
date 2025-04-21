from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from .models import Project

class ProjectCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    data = request.data.copy()
    serializer = ProjectSerializer(data=data)
    if serializer.is_valid():
      # ① IDを確定させるために owner だけで保存（画像はまだ）
      project = Project.objects.create(
          name=data["name"],
          description=data.get("description", ""),
          owner=request.user
      )

      # ② サムネイルがあるなら保存
      if "thumbnail" in request.FILES:
          project.thumbnail = request.FILES["thumbnail"]
          project.save()

      return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
