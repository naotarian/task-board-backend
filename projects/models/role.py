from django.db import models
from .project import ULIDField
from shared.models.soft_delete import SoftDeleteModel

class Role(SoftDeleteModel):
  id = ULIDField(primary_key=True)
  name = models.CharField(max_length=50, unique=True)  # 英語名（ロジック用）
  display_name = models.CharField(max_length=50)       # 日本語表示名（画面用）
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.display_name
