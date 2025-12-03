from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Povežemo Pydantic field z env variablo (validation_alias)
    pg_host: str = Field(validation_alias="PGHOST")
    pg_user: str = Field(validation_alias="PGUSER")
    pg_password: str = Field(validation_alias="PGPASSWORD")
    pg_port: int = Field(5432, validation_alias="PGPORT")
    pg_database: str = Field(validation_alias="PGDATABASE")

    partner_grpc_host: str = Field(validation_alias="PARTNER_GRPC_HOST")
    partner_grpc_port: int = Field(50051, validation_alias="PARTNER_GRPC_PORT")

    # .env podpora (opcijsko, ampak zelo uporabno)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # če imaš še kakšne druge env spremenljivke, jih ignorira
    )


settings = Settings()
