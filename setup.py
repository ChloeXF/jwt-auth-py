from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="jwt_auths",
    version='0.0.5',
    url='https://github.com/ChloeXF/jwt-auth-py',
    packages=['jwt_auth'],
    install_requires=[
        "Django>=2.0.5",
        "djangorestframework>=3.8.2",
        "PyJWT>=1.6.4",
    ],
)
