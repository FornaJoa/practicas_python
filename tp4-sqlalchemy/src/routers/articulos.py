from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from database import get_db
from models.articulos import Articulo
from models.proveedores import Proveedor
from schemas.articulos import ArticuloCreateSchema, ArticuloSchema, ArticuloUpdateSchema

router = APIRouter()

not_found = {
    404: {
        "description": "Artículo no encontrado en el sistema",
        "content": {
            "application/json": {
                "example": {"detail": "Artículo no encontrado"}
            }
        },
    },
}


def _validar_proveedor(db: Session, proveedor_id: int) -> None:
    if db.get(Proveedor, proveedor_id) is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@router.get("/", response_model=list[ArticuloSchema])
async def get_articulos(db: Session = Depends(get_db)):
    return db.query(Articulo).all()


@router.get("/{id}", responses=not_found, response_model=ArticuloSchema)
async def get_articulo_by_id(
    id: Annotated[int, Path(gt=0, description="ID del articulo que deseas buscar")],
    db: Session = Depends(get_db),
):
    articulo = db.get(Articulo, id)
    if articulo is not None:
        return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")


@router.post("/", response_model=ArticuloSchema)
async def post_articulo(
    articulo_nuevo: ArticuloCreateSchema,
    db: Session = Depends(get_db),
):
    _validar_proveedor(db, articulo_nuevo.proveedor_id)
    articulo_db = Articulo(
        nombre=articulo_nuevo.nombre,
        precio=articulo_nuevo.precio,
        modelo=articulo_nuevo.modelo,
        activo=articulo_nuevo.activo,
        proveedor_id=articulo_nuevo.proveedor_id,
    )
    db.add(articulo_db)
    db.commit()
    db.refresh(articulo_db)
    return articulo_db


@router.delete("/{id}", responses=not_found, response_model=list[ArticuloSchema])
async def delete_articulo_by_id(
    id: Annotated[int, Path(gt=0, description="ID del articulo a eliminar")],
    db: Session = Depends(get_db),
    logico: Annotated[
        bool,
        Query(description="Aplicar borrado logico? (True = Desactivar / False = Borrado físico)"),
    ] = False,
):
    articulo = db.get(Articulo, id)
    if articulo is not None:
        if logico:
            articulo.activo = False
            db.commit()
        else:
            db.delete(articulo)
            db.commit()
        return db.query(Articulo).all()
    raise HTTPException(status_code=404, detail="Artículo no encontrado")


@router.put("/{id}", responses=not_found, response_model=ArticuloSchema)
async def put_articulo_by_id(
    id: Annotated[int, Path(gt=0, description="ID del articulo a modificar")],
    articulo_actualizado: ArticuloUpdateSchema,
    db: Session = Depends(get_db),
):
    articulo = db.get(Articulo, id)
    if articulo is not None:
        _validar_proveedor(db, articulo_actualizado.proveedor_id)
        articulo.nombre = articulo_actualizado.nombre
        articulo.precio = articulo_actualizado.precio
        articulo.modelo = articulo_actualizado.modelo
        articulo.activo = articulo_actualizado.activo
        articulo.proveedor_id = articulo_actualizado.proveedor_id
        db.commit()
        db.refresh(articulo)
        return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")
