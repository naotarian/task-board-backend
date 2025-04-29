from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
import os
import logging

User = get_user_model()

logger = logging.getLogger('development')

class PasswordResetView(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = []

	def post(self, request):
		identifier = request.data.get('email')

		if not identifier:
			return Response({'error': 'メールアドレスまたはユーザー名を入力してください'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			if '@' in identifier:
				user = User.objects.get(email=identifier)
			else:
				user = User.objects.get(username=identifier)
		except User.DoesNotExist:
			# セキュリティ上、存在しなくても成功レスポンスを返す
			return Response({'message': 'リセットメールを送信しました'}, status=status.HTTP_200_OK)

		token = default_token_generator.make_token(user)
		uid = urlsafe_base64_encode(force_bytes(user.pk))

		frontend_url = os.getenv('FRONTEND_URL', 'https://localhost')  # 環境変数で管理
		reset_link = f"{frontend_url}/reset-password?uid={uid}&token={token}"

		send_mail(
			subject="パスワードリセットリンク",
			message=f"以下のリンクからパスワードをリセットしてください：\n{reset_link}",
			from_email=None,
			recipient_list=[user.email],
		)

		logger.info(f'パスワードリセットメール送信: {user.email}')

		return Response({'message': 'リセットメールを送信しました'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [AllowAny]

	def post(self, request):
		uidb64 = request.data.get('uid')
		token = request.data.get('token')
		new_password = request.data.get('new_password')

		if not uidb64 or not token or not new_password:
			return Response({'error': '不正なリクエストです'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (User.DoesNotExist, ValueError, TypeError, OverflowError):
			return Response({'error': 'ユーザーが見つかりません'}, status=status.HTTP_400_BAD_REQUEST)

		if not default_token_generator.check_token(user, token):
			return Response({'error': 'トークンが無効または期限切れです'}, status=status.HTTP_400_BAD_REQUEST)

		user.set_password(new_password)
		user.save()

		logger.info(f'パスワードリセット完了: {user.email}')

		return Response({'message': 'パスワードをリセットしました'}, status=status.HTTP_200_OK)
