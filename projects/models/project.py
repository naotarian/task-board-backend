from django.db import models
import ulid
import os
from shared.models.soft_delete import SoftDeleteModel

def generate_ulid():
  return ulid.new().str

def project_thumbnail_upload_to(instance, filename):
  ext = os.path.splitext(filename)[1]
  unique_name = f"{ulid.new()}{ext}"
  return f"projects/{instance.id}/thumbnails/{unique_name}"

class ULIDField(models.CharField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("max_length", 26)
    kwargs.setdefault("default", generate_ulid)
    kwargs.setdefault("editable", False)
    kwargs.setdefault("unique", True)
    super().__init__(*args, **kwargs)

class Project(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  thumbnail = models.ImageField(
    upload_to=project_thumbnail_upload_to,
    null=True,
    blank=True
  )
  owner = models.ForeignKey(
    "users.User",
    on_delete=models.CASCADE,
    related_name="owned_projects"
  )
  is_archived = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  _soft_delete_related = ["members"]

  def __str__(self):
    return self.name
