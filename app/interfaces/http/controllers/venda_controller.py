from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.venda_dto import EfetuarVendaInput, VeiculoVendaOutput, VendaOutput, WebhookInput
from app.application.use_cases.efetuar_venda import EfetuarVendaUseCase
from app.application.use_cases.listar_veiculos_venda import ListarVeiculosVendaUseCase
from app.application.use_cases.listar_veiculos_vendidos import ListarVeiculosVendidosUseCase
from app.application.use_cases.processar_webhook import ProcessarWebhookUseCase
from app.core.exceptions import DomainException, VeiculoNotFoundException, VendaNotFoundException
from app.domain.repositories.venda_repository import VendaRepository
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.http.vehicle_catalog_client import VehicleCatalogClient
from app.interfaces.http.dependencies import get_catalog_client, get_redis_cache, get_venda_repository

router = APIRouter()


@router.get("/veiculos/venda", response_model=list[VeiculoVendaOutput])
async def listar_venda(
    catalog_client: VehicleCatalogClient = Depends(get_catalog_client),
    cache: RedisCache = Depends(get_redis_cache),
):
    use_case = ListarVeiculosVendaUseCase(catalog_client, cache)
    try:
        return await use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar catálogo: {str(e)}")


@router.post("/vendas", response_model=VendaOutput, status_code=201)
async def efetuar_venda(
    input_dto: EfetuarVendaInput,
    repository: VendaRepository = Depends(get_venda_repository),
    catalog_client: VehicleCatalogClient = Depends(get_catalog_client),
):
    use_case = EfetuarVendaUseCase(repository, catalog_client)
    try:
        return await use_case.execute(input_dto)
    except VeiculoNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/webhook/pagamento", response_model=VendaOutput)
async def webhook_pagamento(
    input_dto: WebhookInput,
    repository: VendaRepository = Depends(get_venda_repository),
    catalog_client: VehicleCatalogClient = Depends(get_catalog_client),
):
    use_case = ProcessarWebhookUseCase(repository, catalog_client)
    try:
        return await use_case.execute(input_dto)
    except VendaNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/veiculos/vendidos", response_model=list[VendaOutput])
def listar_vendidos(
    repository: VendaRepository = Depends(get_venda_repository),
):
    use_case = ListarVeiculosVendidosUseCase(repository)
    return use_case.execute()
