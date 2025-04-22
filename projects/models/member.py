from django.db import models
from .project import Project, ULIDField
from users.models import User
from shared.models.soft_delete import SoftDeleteModel

class ProjectMember(SoftDeleteModel):
  id = ULIDField(primary_key=True)  # ← これを追加
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_members")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  _soft_delete_related = ["roles"]

  class Meta:
    unique_together = ('project', 'user')

  def __str__(self):
    return f"{self.user} in {self.project}"
