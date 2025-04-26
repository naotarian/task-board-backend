from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from organizations.models import Organization, OrganizationUser
import logging

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # loggerを取得
        logger = logging.getLogger('development')

        # リクエストオブジェクトを取得
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError('リクエスト情報が取得できません')

        # サブドメインをヘッダーから取得
        subdomain = request.headers.get('x-subdomain')
        logger.info(f'サブドメイン: {subdomain}')

        if not subdomain:
            raise serializers.ValidationError('サブドメインが送信されていません')

        # ローカル開発用例外
        if subdomain == 'localhost':
            return data

        # サブドメインから組織取得
        try:
            organization = Organization.objects.get(sub_domain=subdomain)
        except Organization.DoesNotExist:
            raise serializers.ValidationError('組織が存在しません')

        user = self.user  # SimpleJWTが認証したユーザー
        logger.info(f'ログイン試行ユーザー: {user.username}')

        # 中間テーブル（OrganizationUser）で所属チェック
        if not OrganizationUser.objects.filter(user=user, organization=organization).exists():
            raise serializers.ValidationError('この組織に所属していません')

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
