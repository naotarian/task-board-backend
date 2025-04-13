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
    serializer = ProjectSerializer(data=request.data)

    if serializer.is_valid():
      project = serializer.save(owner=request.user)
      return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, pk):
    project = get_object_or_404(Project, pk=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)
