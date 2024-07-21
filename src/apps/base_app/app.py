from litestar import Litestar
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from apps.base_app.routers import app_router
from db.dependecies import get_uow
from db.postgres.dependecies import get_async_session

app = Litestar(
    openapi_config=OpenAPIConfig(
        title="Litestar API",
        version="0.0.1",
        render_plugins=[SwaggerRenderPlugin()],
    ),
    dependencies={
        "injected_uow": Provide(get_uow),
    },
)
app.register(app_router)
