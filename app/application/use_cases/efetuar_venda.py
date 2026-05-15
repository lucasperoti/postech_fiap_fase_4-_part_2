from uuid import UUID

from app.application.dto.venda_dto import EfetuarVendaInput, VendaOutput
from app.core.exceptions import VeiculoJaVendidoError, VeiculoNotFoundException
from app.domain.enums.veiculo_status import VeiculoStatus
from app.domain.entities.venda import Venda
from app.domain.repositories.venda_repository import VendaRepository
from app.infrastructure.http.vehicle_catalog_client import VehicleCatalogClient


class EfetuarVendaUseCase:
    def __init__(self, venda_repository: VendaRepository, catalog_client: VehicleCatalogClient):
        self._venda_repository = venda_repository
        self._catalog_client = catalog_client

    async def execute(self, input_dto: EfetuarVendaInput) -> VendaOutput:
        veiculo = await self._catalog_client.buscar_por_id(input_dto.veiculo_id)
        if not veiculo:
            raise VeiculoNotFoundException(f"Veículo {input_dto.veiculo_id} não encontrado")

        if veiculo.status != VeiculoStatus.DISPONIVEL:
            raise VeiculoJaVendidoError(f"Veículo não disponível para compra (status: {veiculo.status})")

        venda = Venda(
            veiculo_id=input_dto.veiculo_id,
            cpf_comprador=input_dto.cpf_comprador,
            preco_snapshot=veiculo.preco,
            marca_snapshot=veiculo.marca,
            modelo_snapshot=veiculo.modelo,
            ano_snapshot=veiculo.ano,
            codigo_pagamento=input_dto.codigo_pagamento,
        )
        venda_salva = self._venda_repository.salvar(venda)
        return self._to_output(venda_salva)

    def _to_output(self, venda: Venda) -> VendaOutput:
        return VendaOutput(
            id=venda.id,
            veiculo_id=venda.veiculo_id,
            cpf_comprador=venda.cpf_comprador,
            data_venda=venda.data_venda,
            status=venda.status,
            codigo_pagamento=venda.codigo_pagamento,
            preco_snapshot=venda.preco_snapshot,
            marca_snapshot=venda.marca_snapshot,
            modelo_snapshot=venda.modelo_snapshot,
            ano_snapshot=venda.ano_snapshot,
        )
