from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.core.exceptions import DomainException
from app.domain.enums.venda_status import VendaStatus


@dataclass
class Venda:
    veiculo_id: UUID
    cpf_comprador: str
    preco_snapshot: Decimal
    marca_snapshot: str
    modelo_snapshot: str
    ano_snapshot: int
    id: UUID = field(default_factory=uuid4)
    data_venda: datetime = field(default_factory=datetime.utcnow)
    status: VendaStatus = field(default=VendaStatus.PENDENTE)
    codigo_pagamento: str | None = field(default=None)

    def __post_init__(self):
        if not self.cpf_comprador or len(self.cpf_comprador) < 11:
            raise ValueError("CPF inválido")
        if self.preco_snapshot <= 0:
            raise ValueError("Preço deve ser maior que zero")

    def confirmar(self) -> None:
        if self.status == VendaStatus.CONFIRMADA:
            raise DomainException("Venda já confirmada")
        self.status = VendaStatus.CONFIRMADA

    def cancelar(self) -> None:
        if self.status == VendaStatus.CANCELADA:
            raise DomainException("Venda já cancelada")
        self.status = VendaStatus.CANCELADA
