from django.core.management.base import BaseCommand
from projects.models import Role
import ulid

class Command(BaseCommand):
  help = 'ロールマスターデータを登録します'

  def handle(self, *args, **options):
    roles = [
      {"name": "owner", "display_name": "オーナー"},
      {"name": "admin", "display_name": "管理者"},
      {"name": "member", "display_name": "メンバー"},
      {"name": "viewer", "display_name": "閲覧者"},
    ]

    for role_data in roles:
      if Role.objects.filter(name=role_data["name"]).exists():
        self.stdout.write(self.style.NOTICE(
            f"[roles] '{role_data['name']}' は既に存在します。スキップ"
        ))
        continue

      role = Role.objects.create(
        id=ulid.new().str,
        name=role_data["name"],
        display_name=role_data["display_name"]
      )
      self.stdout.write(self.style.SUCCESS(
        f"[roles] '{role.display_name}' を作成しました（{role.name}）"
      ))
