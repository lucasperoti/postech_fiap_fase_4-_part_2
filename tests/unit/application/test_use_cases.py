import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import Mock, AsyncMock

from app.application.dto.venda_dto import EfetuarVendaInput, WebhookInput
from app.application.use_cases.efetuar_venda import EfetuarVendaUseCase
from app.application.use_cases.listar_veiculos_venda import ListarVeiculosVendaUseCase
from app.application.use_cases.listar_veiculos_vendidos import ListarVeiculosVendidosUseCase
from app.application.use_cases.processar_webhook import ProcessarWebhookUseCase
from app.core.exceptions import VeiculoJaVendidoError, VeiculoNotFoundException, VendaNotFoundException
from app.domain.entities.venda import Venda
from app.domain.enums.venda_status import VendaStatus


class TestListarVeiculosVendaUseCase:
    @pytest.mark.asyncio
    async def test_execute_com_cache(self):
        client = Mock()
        cache = Mock()
        cache.get.return_value = [
            {"id": str(uuid4()), "marca": "Fiat", "modelo": "Uno", "ano": 2020, "cor": "Branco", "preco": "30000", "status": "DISPONIVEL"}
        ]
        
        use_case = ListarVeiculosVendaUseCase(client, cache)
        result = await use_case.execute()
        
        assert len(result) == 1
        assert not client.listar_disponiveis.called

    @pytest.mark.asyncio
    async def test_execute_sem_cache(self):
        client = Mock()
        client.listar_disponiveis = AsyncMock(return_value=[])
        cache = Mock()
        cache.get.return_value = None
        
        use_case = ListarVeiculosVendaUseCase(client, cache)
        result = await use_case.execute()
        
        assert result == []
        client.listar_disponiveis.assert_called_once()


class TestEfetuarVendaUseCase:
    @pytest.mark.asyncio
    async def test_execute_sucesso(self):
        repo = Mock()
        client = Mock()
        from app.application.dto.venda_dto import VeiculoVendaOutput
        from app.domain.enums.veiculo_status import VeiculoStatus
        veiculo = VeiculoVendaOutput(id=uuid4(), marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"), status=VeiculoStatus.DISPONIVEL)
        client.buscar_por_id = AsyncMock(return_value=veiculo)
        
        venda = Venda(veiculo_id=veiculo.id, cpf_comprador="12345678901", preco_snapshot=Decimal("45000"), marca_snapshot="Fiat", modelo_snapshot="Uno", ano_snapshot=2020)
        repo.salvar.return_value = venda
        
        use_case = EfetuarVendaUseCase(repo, client)
        result = await use_case.execute(EfetuarVendaInput(veiculo_id=veiculo.id, cpf_comprador="12345678901"))
        
        assert result.status == VendaStatus.PENDENTE

    @pytest.mark.asyncio
    async def test_execute_veiculo_nao_encontrado(self):
        repo = Mock()
        client = Mock()
        client.buscar_por_id = AsyncMock(return_value=None)
        
        use_case = EfetuarVendaUseCase(repo, client)
        with pytest.raises(VeiculoNotFoundException):
            await use_case.execute(EfetuarVendaInput(veiculo_id=uuid4(), cpf_comprador="12345678901"))

    @pytest.mark.asyncio
    async def test_execute_veiculo_ja_vendido(self):
        repo = Mock()
        client = Mock()
        from app.application.dto.venda_dto import VeiculoVendaOutput
        from app.domain.enums.veiculo_status import VeiculoStatus
        veiculo = VeiculoVendaOutput(id=uuid4(), marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"), status=VeiculoStatus.VENDIDO)
        client.buscar_por_id = AsyncMock(return_value=veiculo)
        
        use_case = EfetuarVendaUseCase(repo, client)
        with pytest.raises(VeiculoJaVendidoError):
            await use_case.execute(EfetuarVendaInput(veiculo_id=veiculo.id, cpf_comprador="12345678901"))


class TestProcessarWebhookUseCase:
    @pytest.mark.asyncio
    async def test_confirmar_pagamento(self):
        repo = Mock()
        client = Mock()
        client.marcar_vendido = AsyncMock()
        venda = Venda(veiculo_id=uuid4(), cpf_comprador="12345678901", preco_snapshot=Decimal("45000"), marca_snapshot="Fiat", modelo_snapshot="Uno", ano_snapshot=2020, codigo_pagamento="PAY123")
        venda.status = VendaStatus.PENDENTE
        repo.buscar_por_codigo_pagamento.return_value = venda
        repo.salvar.return_value = venda
        
        use_case = ProcessarWebhookUseCase(repo, client)
        result = await use_case.execute(WebhookInput(codigo_pagamento="PAY123", status="CONFIRMADO"))
        
        assert result.status == VendaStatus.CONFIRMADA
        client.marcar_vendido.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancelar_pagamento(self):
        repo = Mock()
        client = Mock()
        venda = Venda(veiculo_id=uuid4(), cpf_comprador="12345678901", preco_snapshot=Decimal("45000"), marca_snapshot="Fiat", modelo_snapshot="Uno", ano_snapshot=2020, codigo_pagamento="PAY123")
        venda.status = VendaStatus.PENDENTE
        repo.buscar_por_codigo_pagamento.return_value = venda
        repo.salvar.return_value = venda
        
        use_case = ProcessarWebhookUseCase(repo, client)
        result = await use_case.execute(WebhookInput(codigo_pagamento="PAY123", status="CANCELADO"))
        
        assert result.status == VendaStatus.CANCELADA

    @pytest.mark.asyncio
    async def test_pagamento_nao_encontrado(self):
        repo = Mock()
        client = Mock()
        repo.buscar_por_codigo_pagamento.return_value = None
        
        use_case = ProcessarWebhookUseCase(repo, client)
        with pytest.raises(VendaNotFoundException):
            await use_case.execute(WebhookInput(codigo_pagamento="INVALID", status="CONFIRMADO"))
