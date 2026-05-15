#!/bin/sh
set -e

# Criar tabelas antes de iniciar a aplicacao
python -c "from app.infrastructure.database.config import Base, engine; Base.metadata.create_all(bind=engine)"

# Iniciar a aplicacao
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
