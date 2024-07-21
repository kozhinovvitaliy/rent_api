from litestar import Router

from apps.middlewares import auth_middleware
from apps.users.router import user_router

app_router = Router(path="api", route_handlers=[user_router])
