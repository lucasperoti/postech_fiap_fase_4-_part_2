from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.enums.veiculo_status import VeiculoStatus
from app.domain.enums.venda_status import VendaStatus


class EfetuarVendaInput(BaseModel):
    veiculo_id: UUID
    cpf_comprador: str = Field(..., min_length=11, max_length=14)
    codigo_pagamento: str | None = Field(None, min_length=1)

    @field_validator("cpf_comprador")
    @classmethod
    def clean_cpf(cls, v: str) -> str:
        return v.replace(".", "").replace("-", "")


class WebhookInput(BaseModel):
    codigo_pagamento: str = Field(..., min_length=1)
    status: Literal["CONFIRMADO", "CANCELADO"]


class VeiculoVendaOutput(BaseModel):
    id: UUID
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: VeiculoStatus


class VendaOutput(BaseModel):
    id: UUID
    veiculo_id: UUID
    cpf_comprador: str
    data_venda: datetime
    status: VendaStatus
    codigo_pagamento: str | None
    preco_snapshot: Decimal
    marca_snapshot: str
    modelo_snapshot: str
    ano_snapshot: int
