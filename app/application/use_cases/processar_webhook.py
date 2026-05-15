from app.application.dto.venda_dto import VendaOutput, WebhookInput
from app.core.exceptions import PagamentoJaProcessadoError, VendaNotFoundException
from app.domain.enums.venda_status import VendaStatus
from app.domain.repositories.venda_repository import VendaRepository
from app.infrastructure.http.vehicle_catalog_client import VehicleCatalogClient


class ProcessarWebhookUseCase:
    def __init__(self, venda_repository: VendaRepository, catalog_client: VehicleCatalogClient):
        self._venda_repository = venda_repository
        self._catalog_client = catalog_client

    async def execute(self, input_dto: WebhookInput) -> VendaOutput:
        venda = self._venda_repository.buscar_por_codigo_pagamento(input_dto.codigo_pagamento)
        
        if not venda:
            raise VendaNotFoundException(f"Pagamento {input_dto.codigo_pagamento} não encontrado")

        if venda.status == VendaStatus.CONFIRMADA and input_dto.status == "CONFIRMADO":
            return self._to_output(venda)
        if venda.status == VendaStatus.CANCELADA and input_dto.status == "CANCELADO":
            return self._to_output(venda)

        if input_dto.status == "CONFIRMADO":
            venda.confirmar()
            await self._catalog_client.marcar_vendido(venda.veiculo_id)
        elif input_dto.status == "CANCELADO":
            venda.cancelar()

        venda_atualizada = self._venda_repository.salvar(venda)
        return self._to_output(venda_atualizada)

    def _to_output(self, venda) -> VendaOutput:
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
