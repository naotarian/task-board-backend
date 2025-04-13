from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={"min_length": "パスワードは8文字以上にしてください"}
    )
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=16)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=16)

    class Meta:
      model = User
      fields = ["username", "email", "password", "password_confirm", "first_name", "last_name"]

    def validate_username(self, value):
      if len(value) > 16:
          raise serializers.ValidationError("ユーザー名は16文字以内で入力してください")
      if User.objects.filter(username=value).exists():
          raise serializers.ValidationError("このユーザー名はすでに使用されています")
      return value

    def validate_email(self, value):
      if User.objects.filter(email=value).exists():
          raise serializers.ValidationError("このメールアドレスはすでに使用されています")
      return value

    def validate_password(self, value):
      if not re.match(r"^[a-zA-Z0-9]+$", value):
          raise serializers.ValidationError("パスワードは半角英数字のみ使用できます")
      return value

    def validate(self, data):
      if data["password"] != data["password_confirm"]:
          raise serializers.ValidationError("パスワードが一致しません")
      return data

    def create(self, validated_data):
      validated_data.pop("password_confirm")
      password = validated_data.pop("password")

      user = User.objects.create_user(**validated_data)
      user.set_password(password)
      user.verified_at = None
      user.save()
      return user
