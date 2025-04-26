from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from organizations.models import OrganizationUser, OrganizationUserRole, OrganizationRole
from organizations.serializers.organization_create_serializer import OrganizationCreateSerializer
from organizations.constants.role_name import OrganizationRoleName

class OrganizationCreateView(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = OrganizationCreateSerializer

  @transaction.atomic
  def perform_create(self, serializer):
    # ① Organization を保存
    organization = serializer.save()

    # ② 作成者を OrganizationUser として登録
    organization_user = OrganizationUser.objects.create(
      organization=organization,
      user=self.request.user,
    )

    # ③ owner ロールを取得
    try:
      owner_role = OrganizationRole.objects.get(name=OrganizationRoleName.OWNER)
    except OrganizationRole.DoesNotExist:
      raise Exception(f"ロール '{OrganizationRoleName.OWNER}' が見つかりません")

    # ④ OrganizationUserRole を作成
    OrganizationUserRole.objects.create(
      organization_user=organization_user,
      role=owner_role,
    )

    # ✅ レスポンスデータをカスタムする場合は serializer.save() ではなくここで明示する
    self.response_data = {
      "id": organization.id,
      "name": organization.name,
      "description": organization.description,
      "sub_domain": organization.sub_domain,
    }

  def create(self, request, *args, **kwargs):
    """通常の create をオーバーライドしてカスタムレスポンス"""
    response = super().create(request, *args, **kwargs)
    return Response(self.response_data, status=status.HTTP_201_CREATED)
