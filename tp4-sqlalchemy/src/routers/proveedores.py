from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from database import get_db
from models.proveedores import Proveedor
from schemas.proveedores import ProveedorCreateSchema, ProveedorSchema

router = APIRouter()

not_found = {
    404: {
        "description": "Proveedor no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Proveedor no encontrado"}
            }
        },
    },
}


@router.get("/", response_model=list[ProveedorSchema])
async def get_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all()


@router.get("/{id}", responses=not_found, response_model=ProveedorSchema)
async def get_proveedor_by_id(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
):
    proveedor = db.get(Proveedor, id)
    if proveedor is not None:
        return proveedor
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@router.post("/", response_model=ProveedorSchema)
async def post_proveedor(
    proveedor_nuevo: ProveedorCreateSchema,
    db: Session = Depends(get_db),
):
    proveedor_db = Proveedor(nombre=proveedor_nuevo.nombre)
    db.add(proveedor_db)
    db.commit()
    db.refresh(proveedor_db)
    return proveedor_db


@router.delete("/{id}", responses=not_found, response_model=list[ProveedorSchema])
async def delete_proveedor(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
):
    proveedor = db.get(Proveedor, id)
    if proveedor is not None:
        db.delete(proveedor)
        db.commit()
        return db.query(Proveedor).all()
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@router.put("/{id}", responses=not_found, response_model=ProveedorSchema)
async def put_proveedor(
    id: Annotated[int, Path(gt=0)],
    proveedor_actualizado: ProveedorCreateSchema,
    db: Session = Depends(get_db),
):
    proveedor = db.get(Proveedor, id)
    if proveedor is not None:
        proveedor.nombre = proveedor_actualizado.nombre
        db.commit()
        db.refresh(proveedor)
        return proveedor
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")
