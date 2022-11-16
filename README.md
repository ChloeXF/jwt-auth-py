jwt-auth-py
=====

委托模式的认证。两个服务端直接的交互，委托给其他方（如前端）进行，保证服务端对前端的信赖。

使用场景：当前端页面访问后端服务A时，服务A需要访问服务B获得数据。

如果想将访问服务B的请求委托给前端，存在信赖问题。jwt-auth-py 主要解决该问题。

>> 注意：使用 jwt 对参数 encode 的时候，不能有敏感数据或者暴露代码

依赖
----------

python:3.8.9

Django>=2.0.5

djangorestframework>=3.8.2

PyJWT>=1.6.4

安装
----------

pip install -U jwt_auths

Install and update using `pip`_:

.. code-block:: text

    $ pip install -U jwt_auths

.. _pip: https://pip.pypa.io/en/stable/getting-started/


例子
----------------

.. code-block:: python

    # 两边服务后端创建相同的 Token，用于交互
    
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    
    user = User(username='TEST-JWT-AUTH-PY')
    user.save()
    key = uuid.uuid4().hex
    Token.objects.create(user=user, key=key)
    print('TEST-JWT-AUTH-PY', key)
    
    
.. code-block:: python

    # rest framework 中设置 authentication_classes 认证
    
    from rest_framework.viewsets import ViewSet
    from rest_framework.serializers import Serializer
    from jwt_auth.authentication import JWTTokenAuthentication
    from jwt_auth.response import JwtResponse
    
    @action(methods=['post'], detail=False, authentication_classes=(JWTTokenAuthentication,))
    def test(self, request, *args, **kwargs):  # noqa
        return JwtResponse({'t': 1})

    # 发送请求：
    import requests
    from jwt_auth.request import set_jwt_for_data
    data = {'t': 1}
    # username 值为 USER_MODE 中的 username; key 值为 Token 中的 key
    set_jwt_for_data(username='TEST-JWT-AUTH-PY', key='{key}', data)
    requests.post('/test', data)
