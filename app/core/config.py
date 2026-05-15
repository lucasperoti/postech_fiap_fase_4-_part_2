from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vehicle Sales API"
    debug: bool = False
    database_url: str = "postgresql+psycopg2://postgres:postgres@sales-db:5432/sales_db"
    redis_url: str = "redis://redis:6379/0"
    catalog_service_url: str = "http://vehicle-catalog:8000"
    
    class Config:
        env_file = ".env"


settings = Settings()
