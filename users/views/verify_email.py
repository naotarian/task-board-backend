from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.timezone import now
import logging
User = get_user_model()

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VerifyEmailView(APIView):
  def get(self, request):
    uidb64 = request.query_params.get("uid")
    token = request.query_params.get("token")
    logger = logging.getLogger('development')

    if not uidb64 or not token:
      return Response({"error": "無効なリクエストです"}, status=status.HTTP_400_BAD_REQUEST)
    token = token.rstrip('/')

    try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      logger.info(f'[Verify] デコードされたuid: {uid}')
      user = User.objects.get(pk=uid)

      logger.info(f'[Verify] email: {user.email}')
      logger.info(f'[Verify] password_hash: {user.password}')
      logger.info(f'[Verify] last_login: {user.last_login}')
      logger.info(f'[Verify] is_active: {user.is_active}')
      logger.info(f'[Verify] 検証するトークン: {token}')
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
      return Response({"error": "ユーザーが見つかりません"}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
      user.verified_at = now()
      user.save()
      user_data = {
          "id": user.id,
          "username": user.username,
          "email": user.email,
          "first_name": user.first_name,
          "last_name": user.last_name,
          "verified_at": user.verified_at,
      }

      return Response({"message": "メールアドレスが認証されました", "user": user_data}, status=status.HTTP_200_OK)
    else:
      return Response({"error": "トークンが無効または期限切れです"}, status=status.HTTP_400_BAD_REQUEST)
