from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
import logging
User = get_user_model()

class ResendVerificationEmailView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = []

  def post(self, request):
    user = request.user
    logger = logging.getLogger('development')

    if user.verified_at:
        return Response({"error": "すでに認証済みです。"}, status=400)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # 🔥 トークン生成時点の重要なログを残す
    logger.info(f'[Resend] uid: {uid}')
    logger.info(f'[Resend] email: {user.email}')
    logger.info(f'[Resend] password_hash: {user.password}')
    logger.info(f'[Resend] last_login: {user.last_login}')
    logger.info(f'[Resend] is_active: {user.is_active}')
    logger.info(f'[Resend] 生成したトークン: {token}')

    frontend_url = os.getenv('FRONTEND_URL', 'https://localhost')
    verify_url = f"{frontend_url}/verify-email?uid={uid}&token={token}"

    send_mail(
        "【TaskBoard】メールアドレス認証のご案内",
        f"以下のリンクからメールアドレスの認証を行ってください：\n{verify_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

    return Response({"message": "認証メールを再送信しました。"})

