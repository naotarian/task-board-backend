from django.db import models
from django.utils import timezone
from typing import List


class SoftDeleteQuerySet(models.QuerySet):
  def delete(self):
    return super().update(deleted_at=timezone.now())

  def hard_delete(self):
    return super().delete()

  def alive(self):
    return self.filter(deleted_at__isnull=True)

  def dead(self):
    return self.exclude(deleted_at__isnull=True)


class SoftDeleteManager(models.Manager):
  def get_queryset(self):
    return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
  deleted_at = models.DateTimeField(null=True, blank=True)

  # 有効な（論理削除されていない）レコードのみ取得
  objects = SoftDeleteManager()
  # 全レコード取得（論理削除されたもの含む）
  all_objects = models.Manager()

  # 論理削除時にカスケード対象のrelated_nameを定義
  _soft_delete_related: List[str] = []

  def delete(self, using=None, keep_parents=False):
    # 論理削除のカスケード処理
    for related_name in getattr(self, "_soft_delete_related", []):
      related_manager = getattr(self, related_name, None)
      if related_manager and hasattr(related_manager, "all"):
        for related_obj in related_manager.all():
          if isinstance(related_obj, SoftDeleteModel):
            related_obj.delete(using=using)

    self.deleted_at = timezone.now()
    self.save(update_fields=["deleted_at"])

  def restore(self):
    self.deleted_at = None
    self.save(update_fields=["deleted_at"])

  def hard_delete(self, using=None, keep_parents=False):
    super().delete(using=using, keep_parents=keep_parents)

  class Meta:
    abstract = True
