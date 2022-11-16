jwt-auth-py
=====

委托模式的认证。两个服务端直接的交互，委托给其他方（如前端）进行，保证服务端对前端的信赖。

使用场景：当前端页面访问后端服务A时，服务A需要访问服务B获得数据。

如果想将访问服务B的请求委托给前端，存在信赖问题。jwt-auth-py 主要解决该问题。

>> 注意：后端服务给前端的数据，不能有敏感数据或者暴露代码

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

