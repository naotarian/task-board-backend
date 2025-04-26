from django.db import models
from shared.models.soft_delete import SoftDeleteModel
from shared.models.ulid_field import ULIDField

class OrganizationUserRole(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  organization_user = models.ForeignKey(
    "organizations.OrganizationUser",
    on_delete=models.CASCADE,
    related_name="organization_roles",
  )
  role = models.ForeignKey(
    "organizations.OrganizationRole",
    on_delete=models.CASCADE,
  )
  assigned_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.organization_user} - {self.role}"

