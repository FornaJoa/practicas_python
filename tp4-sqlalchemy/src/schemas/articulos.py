from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

STR_NOMBRE = Annotated[str, Field(max_length=50, description="Nombre del periférico")]
STR_MODELO = Annotated[str, Field(max_length=50, description="Modelo del periférico")]
PRECIO_VALOR = Annotated[float, Field(gt=0, lt=1000000, description="Precio del periférico")]
BOOL_ACTIVO = Annotated[bool, Field(description="¿El periférico se encuentra activo?")]
ID_PROVEEDOR = Annotated[int, Field(gt=0, description="ID del proveedor (FK)")]


class ArticuloSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(gt=0, description="ID del artículo")]
    nombre: STR_NOMBRE
    precio: PRECIO_VALOR
    modelo: STR_MODELO
    activo: BOOL_ACTIVO = True
    proveedor_id: ID_PROVEEDOR


class ArticuloCreateSchema(BaseModel):
    nombre: STR_NOMBRE
    precio: PRECIO_VALOR
    modelo: STR_MODELO
    activo: BOOL_ACTIVO = True
    proveedor_id: ID_PROVEEDOR


class ArticuloUpdateSchema(BaseModel):
    nombre: STR_NOMBRE
    precio: PRECIO_VALOR
    modelo: STR_MODELO
    activo: BOOL_ACTIVO = True
    proveedor_id: ID_PROVEEDOR
