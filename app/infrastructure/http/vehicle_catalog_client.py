from uuid import UUID

import httpx

from app.application.dto.venda_dto import VeiculoVendaOutput
from app.core.config import settings


class VehicleCatalogClient:
    def __init__(self, base_url: str = None):
        self._base_url = base_url or settings.catalog_service_url
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=10.0)

    async def listar_disponiveis(self) -> list[VeiculoVendaOutput]:
        response = await self._client.get("/internal/veiculos/disponiveis")
        response.raise_for_status()
        data = response.json()
        return [VeiculoVendaOutput(**item) for item in data]

    async def buscar_por_id(self, veiculo_id: UUID) -> VeiculoVendaOutput | None:
        # Vamos usar o endpoint de listagem e filtrar, ou criar um novo endpoint
        # Para simplificar, vamos assumir que existe um GET /internal/veiculos/{id}
        # Se não existir, precisamos adicionar no catalog
        # Por enquanto, vamos criar um endpoint genérico
        response = await self._client.get(f"/internal/veiculos/{veiculo_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return VeiculoVendaOutput(**response.json())

    async def marcar_vendido(self, veiculo_id: UUID) -> None:
        response = await self._client.put(f"/internal/veiculos/{veiculo_id}/vender")
        response.raise_for_status()

    async def close(self):
        await self._client.aclose()
