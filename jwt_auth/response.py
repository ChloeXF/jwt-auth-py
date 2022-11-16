"""
The Response class is similar to HTTPResponse

"""
from __future__ import unicode_literals

from rest_framework.response import Response

from jwt_auth.request import set_jwt_for_data


class JwtResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, jwt_request, *args, **kwargs):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """

        super().__init__(*args, **kwargs)

        set_jwt_for_data(
            jwt_request.user.username,
            jwt_request.auth.key,
            self.data,
        )
