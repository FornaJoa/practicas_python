from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models.articulos import Articulo  
from models.proveedores import Proveedor  
from routers.articulos import router as articulos_router
from routers.proveedores import router as proveedores_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "TP4 - SQLAlchemy + SQLite"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proveedores_router, tags=["Proveedores"], prefix="/proveedores")
app.include_router(articulos_router, tags=["Artículos"], prefix="/articulos")
