from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.venda import Venda


class VendaRepository(ABC):
    @abstractmethod
    def salvar(self, venda: Venda) -> Venda:
        pass

    @abstractmethod
    def buscar_por_id(self, venda_id: UUID) -> Venda | None:
        pass

    @abstractmethod
    def buscar_por_codigo_pagamento(self, codigo: str) -> Venda | None:
        pass

    @abstractmethod
    def listar_vendidos(self) -> list[Venda]:
        pass
