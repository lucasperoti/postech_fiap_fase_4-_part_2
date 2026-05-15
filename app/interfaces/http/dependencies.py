from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.repositories.venda_repository import VendaRepository
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.database.config import get_db
from app.infrastructure.database.repositories.sql_venda_repository import SQLVendaRepository
from app.infrastructure.http.vehicle_catalog_client import VehicleCatalogClient


def get_venda_repository(db: Session = Depends(get_db)) -> VendaRepository:
    return SQLVendaRepository(db)


def get_catalog_client() -> VehicleCatalogClient:
    return VehicleCatalogClient()


def get_redis_cache() -> RedisCache:
    return RedisCache()
