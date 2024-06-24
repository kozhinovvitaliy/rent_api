from litestar.middleware.base import DefineMiddleware
from .auth import JWTAuthenticationMiddleware

auth_middleware = DefineMiddleware(JWTAuthenticationMiddleware)
