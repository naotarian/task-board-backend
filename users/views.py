from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.timezone import now
from django.conf import settings

User = get_user_model()
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'verified_at': user.verified_at,
        })


class PasswordResetView(APIView):
  def post(self, request):
    identifier = request.data.get('email')

    if not identifier:
        return Response({'error': 'メールアドレスまたはユーザー名を入力してください'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # @ が含まれてたら email として探す、それ以外は username
        if '@' in identifier:
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(username=identifier)

    except User.DoesNotExist:
        # 存在しなくてもセキュリティ上同じレスポンスにする
        return Response({'message': 'リセットメールを送信しました'}, status=status.HTTP_200_OK)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://localhost:3000/reset-password?uid={uid}&token={token}"

    send_mail(
      subject="パスワードリセットリンク",
      message=f"以下のリンクからパスワードをリセットしてください：\n{reset_link}",
      from_email=None,
      recipient_list=[user.email],
    )

    return Response({'message': 'リセットメールを送信しました'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
  def post(self, request):
    uidb64 = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")

    if not uidb64 or not token or not new_password:
        return Response({"error": "不正なリクエストです"}, status=400)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "ユーザーが見つかりません"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "トークンが無効または期限切れです"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "パスワードをリセットしました"}, status=200)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 認証メール送信準備
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verify_url = f"http://localhost:3000/verify-email?uid={uid}&token={token}"

            send_mail(
                 "【TaskBoard】メールアドレス認証のご案内",
                f"以下のリンクからメールアドレスの認証を行ってください：\n{verify_url}",
                from_email="noreply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({"message": "仮登録が完了しました。メールを確認してください"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uidb64 or not token:
            return Response({"error": "無効なリクエストです"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "ユーザーが見つかりません"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.verified_at = now()
            user.save()
            return Response({"message": "メールアドレスが認証されました"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "トークンが無効または期限切れです"}, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmailView(APIView):
    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"error": "ユーザー名が必要です。"}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "ユーザーが存在しません。"}, status=404)

        if user.verified_at:
            return Response({"error": "すでに認証済みです。"}, status=400)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = f"http://localhost:3000/verify-email?uid={uid}&token={token}"

        send_mail(
            "【TaskBoard】メールアドレス認証のご案内",
            f"以下のリンクからメールアドレスの認証を行ってください：\n{verify_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        return Response({"message": "認証メールを再送信しました。"})
