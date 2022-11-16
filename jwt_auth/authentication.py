"""
Provides various authentication policies.
"""

import jwt
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions


class BaseAuthentication(object):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class JWTTokenAuthentication(BaseAuthentication):
    """
    POST 请求体中，需要包含两个字段
    JWT-AUTH-ACCESS-KEY-ID:     值为 USER_MODE 中的 username
    JWT-PAYLOAD:                值为参数 jwt encode 的结果
    """

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):

        # data 中必须包含参数 JWT-AUTH-ACCESS-KEY-ID，值为 USER_MODE 中的 username
        access_key_id = request.data.get('JWT-AUTH-ACCESS-KEY-ID')
        if not access_key_id:
            return None

        # data 中必须包含参数 JWT-PAYLOAD，值为参数 jwt encode 的结果
        payload = request.data.get('JWT-PAYLOAD')
        if not payload:
            return None

        user, token, data = self.authenticate_credentials(access_key_id, payload)
        request._full_data = data
        return user, token

    def authenticate_credentials(self, access_key_id, payload):
        """
        @param access_key_id:       USER_MODE 中的 username
        @param payload:             参数 jwt encode 后的内容
        """

        model = self.get_model()
        try:
            token = model.objects.get(user__username=access_key_id)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        try:
            data = jwt.decode(
                payload,
                token.key,
                verify=True,
                algorithms='HS256',
                leeway=0,
                options={'verify_exp': True},
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.PermissionDenied(_('Signature has expired'))
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.PermissionDenied(_('Signature verification failed'))

        if not 'exp' in data:
            raise exceptions.PermissionDenied(_('Signature has expired'))

        return (token.user, token, data)
