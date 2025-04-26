from django.db import models
from shared.models.soft_delete import SoftDeleteModel
from shared.models.ulid_field import ULIDField

class OrganizationUser(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  organization = models.ForeignKey(
    "organizations.Organization",
    on_delete=models.CASCADE,
    related_name="organization_users"
  )
  user = models.ForeignKey(
    "users.User",
    on_delete=models.CASCADE,
    related_name="user_organizations"
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("organization", "user")

  def __str__(self):
    return f"{self.user} in {self.organization}"
