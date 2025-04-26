from django.db import models
from shared.models.soft_delete import SoftDeleteModel
from shared.models.ulid_field import ULIDField

class OrganizationRole(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  name = models.CharField(max_length=50, unique=True)
  display_name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.display_name
