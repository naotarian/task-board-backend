
from rest_framework import serializers
from organizations.models import Organization
from rest_framework.validators import UniqueValidator
import re

SUBDOMAIN_REGEX = r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
class OrganizationCreateSerializer(serializers.ModelSerializer):
  name = serializers.CharField(
    max_length=100,
    required=True,
    error_messages={
      "required": "組織名を入力してください。",
      "blank": "組織名を入力してください。",
      "max_length": "組織名は100文字以内で入力してください。",
    }
  )
  description = serializers.CharField(
    max_length=1000,
    required=False,
    allow_blank=True,
    error_messages={
      "max_length": "説明文は1000文字以内で入力してください。",
    }
  )
  sub_domain = serializers.CharField(
    max_length=63,
    min_length=2,
    required=True,
    validators=[
      UniqueValidator(
          queryset=Organization.objects.all(),
          message="このサブドメインは既に使用されています。",
      )
    ],
    error_messages={
      "required": "サブドメインを入力してください。",
      "blank": "サブドメインを入力してください。",
      "min_length": "サブドメインは2文字以上で入力してください。",
      "max_length": "サブドメインは63文字以内で入力してください。",
    },
  )

  class Meta:
    model = Organization
    fields = ['name', 'description', 'sub_domain']

  def validate_sub_domain(self, value):
    if re.search('[A-Z]', value):
      raise serializers.ValidationError("サブドメインは英小文字・数字・ハイフンのみ使用できます。")
    if not re.fullmatch(SUBDOMAIN_REGEX, value):
      raise serializers.ValidationError(
        "サブドメインは英小文字・数字・ハイフンのみ使用でき、ハイフンで開始・終了できません。"
      )
    return value
