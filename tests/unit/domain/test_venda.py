import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.venda import Venda
from app.domain.enums.venda_status import VendaStatus
from app.core.exceptions import DomainException


class TestVendaEntity:
    def test_criar_venda_sucesso(self):
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("45000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
        )
        assert venda.status == VendaStatus.PENDENTE
        assert venda.cpf_comprador == "12345678901"

    def test_criar_venda_cpf_invalido(self):
        with pytest.raises(ValueError, match="CPF inválido"):
            Venda(
                veiculo_id=uuid4(),
                cpf_comprador="123",
                preco_snapshot=Decimal("45000"),
                marca_snapshot="Fiat",
                modelo_snapshot="Uno",
                ano_snapshot=2020,
            )

    def test_confirmar_venda(self):
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("45000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
        )
        venda.confirmar()
        assert venda.status == VendaStatus.CONFIRMADA

    def test_confirmar_venda_ja_confirmada(self):
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("45000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
        )
        venda.confirmar()
        with pytest.raises(DomainException):
            venda.confirmar()

    def test_cancelar_venda(self):
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("45000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
        )
        venda.cancelar()
        assert venda.status == VendaStatus.CANCELADA
