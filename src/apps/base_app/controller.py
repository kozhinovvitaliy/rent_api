from typing import ClassVar

from litestar import Controller

from apps.base_app.service import BaseService


class BaseController(Controller):
    path: str
    service: ClassVar[BaseService]
