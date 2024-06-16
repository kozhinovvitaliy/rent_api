from typing import Type

from litestar import Controller

from apps.base_app.service import BaseService


class BaseController(Controller):
    path: str
    service: Type[BaseService]
