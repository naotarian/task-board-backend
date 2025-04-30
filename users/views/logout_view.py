import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session

# @method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = []

  def get(self, request):
    logger = logging.getLogger('development')
    user = request.user
    if not request.user.is_authenticated:
      logger.info('ログインしていないため、ログアウトできません')
      return Response({'detail': '認証されていません'}, status=status.HTTP_401_UNAUTHORIZED)

    # ログイン中なので、ログアウト実行
    logger.info(f'ログアウトユーザー: {request.user.username}')

    logout(request)
    request.session.flush()  # 念のため完全にセッション破棄

    logger.info('ログアウト成功、セッション破棄')

    return Response({'detail': 'ログアウトしました'}, status=status.HTTP_200_OK)
