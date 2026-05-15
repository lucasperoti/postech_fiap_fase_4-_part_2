# Vehicle Sales API

Microsservico de vendas de veiculos para a plataforma de revenda de veiculos (SOAT Fase 4).

**Repositorio:** https://github.com/lucasperoti/postech_fiap_fase_4-_part_2.git

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy 2.0 + Alembic
- PostgreSQL
- Redis (cache)
- httpx (cliente HTTP)
- pytest + pytest-asyncio + respx

## Como rodar localmente

### Opcao 1: Docker Compose (recomendado)

```bash
# Na raiz do projeto
docker-compose up --build
```

A API estara disponivel em `http://localhost:18081`

### Opcao 2: Localmente com Python

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar banco de dados (PostgreSQL) e Redis
# Edite .env se necessario

# Rodar a aplicacao
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Documentacao da API

- Swagger UI: `http://localhost:18081/docs`
- ReDoc: `http://localhost:18081/redoc`

## Como testar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Rodar testes com cobertura
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

## Endpoints

| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | `/sales/veiculos/venda` | Listar veiculos a venda (com cache Redis) |
| POST | `/sales/vendas` | Efetuar venda |
| POST | `/sales/webhook/pagamento` | Webhook de pagamento |
| GET | `/sales/veiculos/vendidos` | Listar veiculos vendidos |

## Arquitetura

Clean Architecture pragmatica:
- `domain/` - Entidades e regras de negocio puras
- `application/` - Casos de uso e DTOs
- `infrastructure/` - SQLAlchemy, Redis, cliente HTTP
- `interfaces/` - FastAPI controllers

## Comunicacao

Este microsservico se comunica com o `vehicle-catalog` via HTTP para consultar veiculos disponiveis e marcar veiculos como vendidos.
