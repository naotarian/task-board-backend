from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organizations.models import Organization, OrganizationUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
  authentication_classes = []  # デフォルト認証無効化
  permission_classes = []      # パーミッションも無効化
  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')

    # ① サブドメインヘッダーを取得
    subdomain = request.headers.get('x-subdomain')

    if not subdomain:
      return Response({'detail': 'サブドメインが指定されていません。'}, status=status.HTTP_400_BAD_REQUEST)

    # ② 組織を取得
    if subdomain == 'localhost':
      organization = None  # ローカル開発用に特別扱い
    else:
      try:
        organization = Organization.objects.get(sub_domain=subdomain)
      except Organization.DoesNotExist:
        return Response({'detail': '指定された組織が存在しません。'}, status=status.HTTP_404_NOT_FOUND)

    # ③ ユーザー認証
    user = authenticate(request, username=username, password=password)
    if user is None:
      return Response({'detail': 'ユーザー名またはパスワードが間違っています。'}, status=status.HTTP_401_UNAUTHORIZED)

    # ④ 組織所属チェック（localhostの場合はスキップ）
    if organization:
      if not OrganizationUser.objects.filter(user=user, organization=organization).exists():
        return Response({'detail': 'この組織に所属していません。'}, status=status.HTTP_403_FORBIDDEN)

    # ⑤ ログイン処理
    request.session.flush()
    login(request, user)

    return Response({'detail': 'ログイン成功'}, status=status.HTTP_200_OK)
