from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.sql import func

from app.domain.enums.venda_status import VendaStatus
from app.infrastructure.database.config import Base


class VendaModel(Base):
    __tablename__ = "vendas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    veiculo_id = Column(String(36), nullable=False, index=True)
    cpf_comprador = Column(String(14), nullable=False)
    data_venda = Column(DateTime, default=func.now(), nullable=False)
    status = Column(Enum(VendaStatus), default=VendaStatus.PENDENTE, nullable=False)
    codigo_pagamento = Column(String(100), nullable=True, unique=True)
    preco_snapshot = Column(Numeric(10, 2), nullable=False)
    marca_snapshot = Column(String(100), nullable=False)
    modelo_snapshot = Column(String(100), nullable=False)
    ano_snapshot = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
