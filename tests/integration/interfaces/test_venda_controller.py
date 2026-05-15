import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.config import Base, get_db
from app.infrastructure.database.repositories.sql_venda_repository import SQLVendaRepository
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestVendaController:
    def test_listar_vendidos_vazio(self, client):
        response = client.get("/sales/veiculos/vendidos")
        assert response.status_code == 200
        assert response.json() == []

    def test_webhook_pagamento_nao_encontrado(self, client):
        response = client.post("/sales/webhook/pagamento", json={
            "codigo_pagamento": "INVALIDO123",
            "status": "CONFIRMADO",
        })
        assert response.status_code == 404


class TestSQLVendaRepository:
    def test_salvar_e_atualizar(self, db_session):
        from app.domain.entities.venda import Venda
        from uuid import uuid4
        from decimal import Decimal
        from app.domain.enums.venda_status import VendaStatus

        repo = SQLVendaRepository(db_session)
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("50000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
            codigo_pagamento="PAY-TEST-01",
        )
        salva = repo.salvar(venda)
        assert salva.status == VendaStatus.PENDENTE

        # Atualizar
        salva.confirmar()
        atualizada = repo.salvar(salva)
        assert atualizada.status == VendaStatus.CONFIRMADA

    def test_buscar_por_codigo_pagamento(self, db_session):
        from app.domain.entities.venda import Venda
        from uuid import uuid4
        from decimal import Decimal

        repo = SQLVendaRepository(db_session)
        venda = Venda(
            veiculo_id=uuid4(),
            cpf_comprador="12345678901",
            preco_snapshot=Decimal("50000"),
            marca_snapshot="Fiat",
            modelo_snapshot="Uno",
            ano_snapshot=2020,
            codigo_pagamento="PAY-TEST-02",
        )
        repo.salvar(venda)

        encontrada = repo.buscar_por_codigo_pagamento("PAY-TEST-02")
        assert encontrada is not None
        assert encontrada.codigo_pagamento == "PAY-TEST-02"
