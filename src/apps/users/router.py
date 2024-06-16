from litestar import Router

from apps.users.controller import UserController

user_router = Router(path="user", route_handlers=[UserController])
