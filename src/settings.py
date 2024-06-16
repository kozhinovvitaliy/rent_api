from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Postgres(BaseSettings):
    dsn: PostgresDsn = MultiHostUrl(
        "postgresql+asyncpg://vitaliykozhinov:Dbnfkz1996@localhost:5432/rent",
    )

    @property
    def url(self) -> str:
        return str(self.dsn)


class AppSettings(BaseSettings):
    debug: bool = True


class Settings(BaseSettings):
    postgres: Postgres = Postgres()
    app: AppSettings = AppSettings()


settings = Settings()
