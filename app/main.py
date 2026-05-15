from fastapi import FastAPI

from app.interfaces.http.controllers.venda_controller import router as venda_router

app = FastAPI(title="Vehicle Sales API", version="1.0.0")

app.include_router(venda_router, prefix="/sales")


@app.get("/health")
def health():
    return {"status": "ok"}
