"""
The Request class is used as a wrapper around the standard request object.

The wrapped request then offers a richer API, in particular :

    - content automatically parsed according to `Content-Type` header,
      and available as `request.data`
    - full support of PUT method, including support for file uploads
    - form overloading of HTTP method, content type and content
"""

import jwt


def set_jwt_for_data(username, key, data, exp=60):
    """
    @param:username              值为 USER_MODE 中的 username
    @param:key                   值为 Token 中的 key
    @param:data                  值为 请求参数

    data 中添加：
    JWT-AUTH-ACCESS-KEY-ID:     值为 USER_MODE 中的 username
    JWT-PAYLOAD:                值为参数 jwt encode 的结果
    """
    if 'exp' in data:
        raise AssertionError('You can not set exp in data')
    data['exp'] = exp
    payload = jwt.encode(
        data,
        key,
        'HS256',
        {'alg': 'HS256', 'typ': 'JWT'}
    ).decode('utf8')
    data['JWT-AUTH-ACCESS-KEY-ID'] = username
    data['JWT-PAYLOAD'] = payload
