from django.db import models
from django.conf import settings
import ulid

def generate_ulid():
  return ulid.new().str  # ULIDオブジェクトではなくstr型で返す

class ULIDField(models.CharField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("max_length", 26)
    kwargs.setdefault("default", generate_ulid)
    kwargs.setdefault("editable", False)
    kwargs.setdefault("unique", True)
    super().__init__(*args, **kwargs)

# ✅ Projectモデル本体
class Project(models.Model):
  id = ULIDField(primary_key=True)

  # プロジェクト名（必須）
  name = models.CharField(max_length=100)

  # 説明（任意）
  description = models.TextField(blank=True)

  # サムネイル画像（任意）
  thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)

  # オーナー（usersアプリのUserモデルと外部キー）
  owner = models.ForeignKey(
    "users.User",
    on_delete=models.CASCADE,
    related_name="owned_projects"
  )
  is_archived = models.BooleanField(default=False)

  # 作成日時・更新日時（自動設定）
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
