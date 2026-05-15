from decimal import Decimal
from uuid import UUID

from app.domain.entities.venda import Venda
from app.domain.enums.venda_status import VendaStatus
from app.domain.repositories.venda_repository import VendaRepository
from app.infrastructure.database.models.venda_model import VendaModel


class SQLVendaRepository(VendaRepository):
    def __init__(self, db_session):
        self._session = db_session

    def salvar(self, venda: Venda) -> Venda:
        existing = self._session.query(VendaModel).filter_by(id=str(venda.id)).first()
        if existing:
            existing.veiculo_id = str(venda.veiculo_id)
            existing.cpf_comprador = venda.cpf_comprador
            existing.data_venda = venda.data_venda
            existing.status = venda.status
            existing.codigo_pagamento = venda.codigo_pagamento
            existing.preco_snapshot = venda.preco_snapshot
            existing.marca_snapshot = venda.marca_snapshot
            existing.modelo_snapshot = venda.modelo_snapshot
            existing.ano_snapshot = venda.ano_snapshot
            self._session.commit()
            self._session.refresh(existing)
            return self._to_entity(existing)
        
        model = VendaModel(
            id=str(venda.id),
            veiculo_id=str(venda.veiculo_id),
            cpf_comprador=venda.cpf_comprador,
            data_venda=venda.data_venda,
            status=venda.status,
            codigo_pagamento=venda.codigo_pagamento,
            preco_snapshot=venda.preco_snapshot,
            marca_snapshot=venda.marca_snapshot,
            modelo_snapshot=venda.modelo_snapshot,
            ano_snapshot=venda.ano_snapshot,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def buscar_por_id(self, venda_id: UUID) -> Venda | None:
        model = self._session.query(VendaModel).filter_by(id=str(venda_id)).first()
        if model:
            return self._to_entity(model)
        return None

    def buscar_por_codigo_pagamento(self, codigo: str) -> Venda | None:
        model = self._session.query(VendaModel).filter_by(codigo_pagamento=codigo).first()
        if model:
            return self._to_entity(model)
        return None

    def listar_vendidos(self) -> list[Venda]:
        models = (
            self._session.query(VendaModel)
            .filter_by(status=VendaStatus.CONFIRMADA)
            .order_by(VendaModel.preco_snapshot.asc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: VendaModel) -> Venda:
        from uuid import UUID
        return Venda(
            id=UUID(model.id),
            veiculo_id=UUID(model.veiculo_id),
            cpf_comprador=model.cpf_comprador,
            data_venda=model.data_venda,
            status=model.status,
            codigo_pagamento=model.codigo_pagamento,
            preco_snapshot=Decimal(str(model.preco_snapshot)),
            marca_snapshot=model.marca_snapshot,
            modelo_snapshot=model.modelo_snapshot,
            ano_snapshot=model.ano_snapshot,
        )
