from django.db import models
from shared.models.soft_delete import SoftDeleteModel
from shared.models.ulid_field import ULIDField
import ulid
import os

def logo_upload_to(instance, filename):
  ext = os.path.splitext(filename)[1]
  unique_name = f"{ulid.new()}{ext}"
  return f"organizations/{instance.id}/logos/{unique_name}"

class Organization(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  name = models.CharField(max_length=100)
  sub_domain = models.CharField(max_length=100, blank=True, default="", unique=True)
  description = models.TextField(blank=True, null=True)
  logo = models.ImageField(
    upload_to=logo_upload_to,
    null=True,
    blank=True
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
