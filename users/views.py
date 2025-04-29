from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.timezone import now
from organizations.models import OrganizationUser, Organization, OrganizationUserRole
import logging
User = get_user_model()

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

class MeView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = []

  def get(self, request):
    subdomain = request.headers.get('x-subdomain')
    log = logging.getLogger('development')

    if not request.user.is_authenticated:
      return Response({'detail': '認証情報がありません'}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    # logout(request)

    # ① サブドメインがあれば、そのorganizationに所属しているかチェック
    if subdomain and subdomain != "localhost":  # ローカル開発用の例外
      try:
        organization = Organization.objects.get(sub_domain=subdomain)
      except Organization.DoesNotExist:
        log.info('サブドメインに該当する組織が存在しません')
        return Response({'detail': '組織が存在しません'}, status=status.HTTP_400_BAD_REQUEST)

      # 所属しているかチェック
      if not OrganizationUser.objects.filter(user=user, organization=organization).exists():
        log.info('ユーザーがこの組織に所属していません')
        return Response({'detail': 'この組織に所属していません'}, status=status.HTTP_403_FORBIDDEN)

    organization_users = OrganizationUser.objects.filter(user=user).select_related('organization')
    organizations_data = []

    for org_user in organization_users:
      org_user_roles = OrganizationUserRole.objects.filter(
        organization_user=org_user
      ).select_related('role')

      role_display_names = [
        {
          "name": role.role.name,
          "display_name": role.role.display_name,
        }
        for role in org_user_roles
      ]

      organizations_data.append({
        "id": org_user.organization.id,
        "name": org_user.organization.name,
        "subdomain": org_user.organization.sub_domain,
        "logo": request.build_absolute_uri(org_user.organization.logo.url) if org_user.organization.logo else None,
        "roles": role_display_names,
      })

    return Response({
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'verified_at': user.verified_at,
      "organizations": organizations_data,
    })

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


