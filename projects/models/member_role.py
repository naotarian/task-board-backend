from django.db import models
from .member import ProjectMember
from .role import Role
from shared.models.soft_delete import SoftDeleteModel

class ProjectMemberRole(SoftDeleteModel):
  member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, related_name="roles")
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("member", "role")
