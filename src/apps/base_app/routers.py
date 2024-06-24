from litestar import Router

from apps.users.router import user_router
from apps.middlewares import auth_middleware

app_router = Router(path="api", route_handlers=[user_router], middleware=[auth_middleware])
