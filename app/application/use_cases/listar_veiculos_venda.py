from app.application.dto.venda_dto import VeiculoVendaOutput
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.http.vehicle_catalog_client import VehicleCatalogClient


class ListarVeiculosVendaUseCase:
    def __init__(self, catalog_client: VehicleCatalogClient, cache: RedisCache):
        self._catalog_client = catalog_client
        self._cache = cache

    async def execute(self) -> list[VeiculoVendaOutput]:
        cached = self._cache.get("veiculos:disponiveis")
        if cached:
            return [VeiculoVendaOutput(**item) for item in cached]

        veiculos = await self._catalog_client.listar_disponiveis()
        self._cache.set("veiculos:disponiveis", [v.model_dump() for v in veiculos], ttl=60)
        return veiculos
