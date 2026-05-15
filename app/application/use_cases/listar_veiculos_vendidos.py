from app.application.dto.venda_dto import VendaOutput
from app.domain.repositories.venda_repository import VendaRepository


class ListarVeiculosVendidosUseCase:
    def __init__(self, repository: VendaRepository):
        self._repository = repository

    def execute(self) -> list[VendaOutput]:
        vendas = self._repository.listar_vendidos()
        return [self._to_output(v) for v in vendas]

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
