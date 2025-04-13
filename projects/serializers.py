from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
  name = serializers.CharField(
    max_length=24,
    required=True,
    error_messages={
      "required": "プロジェクト名は必須です。",
      "max_length": "プロジェクト名は24文字以内で入力してください。"
    }
  )
  description = serializers.CharField(
    max_length=256,
    required=False,
    allow_blank=True,
    error_messages={
      "max_length": "説明は256文字以内で入力してください。"
    }
  )

  class Meta:
    model = Project
    fields = ['id', 'name', 'description', 'thumbnail', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  def create(self, validated_data):
    # owner は view 側でセットするため除外
    return Project.objects.create(**validated_data)
