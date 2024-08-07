from pydantic import Field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Postgres(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    dsn: PostgresDsn = MultiHostUrl(
        "postgresql+asyncpg://otus:otus@localhost:5432/otus_db",
    )

    @property
    def url(self) -> str:
        return str(self.dsn)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    key: str = Field(..., alias="APP_API_KEY")
    debug: bool = True


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SECURITY_")

    jwt_secret: str = Field(..., alias="SECURITY_JWT")
    jwt_expiration: int = 3600
    algorithm: str = "HS256"


class Settings(BaseSettings):
    postgres: Postgres = Postgres()
    app: AppSettings = AppSettings()
    security: SecuritySettings = SecuritySettings()


settings = Settings()
