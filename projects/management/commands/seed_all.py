from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
  help = 'すべてのマスターデータを一括登録します'

  def handle(self, *args, **options):
    seeds = [
      "seed_roles",
      # 今後追加されるシーダー
      # "seed_categories",
      # "seed_tags",
    ]

    for seed in seeds:
      self.stdout.write(f"\n--- 実行: {seed} ---")
      call_command(seed)


# python manage.py seed_roles
