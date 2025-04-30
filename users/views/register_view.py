from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
import os

User = get_user_model()

class RegisterView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = []

  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()

      # 認証メール送信準備
      token = default_token_generator.make_token(user)
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      frontend_url = os.getenv('FRONTEND_URL', 'https://localhost')
      verify_url = f"{frontend_url}/verify-email?uid={uid}&token={token}"

      send_mail(
        "【TaskBoard】メールアドレス認証のご案内",
        f"以下のリンクからメールアドレスの認証を行ってください：\n{verify_url}",
        from_email="noreply@example.com",
        recipient_list=[user.email],
        fail_silently=False,
      )

      return Response({"message": "仮登録が完了しました。メールを確認してください"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
