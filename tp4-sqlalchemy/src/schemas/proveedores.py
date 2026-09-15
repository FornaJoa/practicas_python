from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

STR_NOMBRE = Annotated[str, Field(max_length=50, description="Nombre del proveedor")]


class ProveedorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(gt=0, description="ID del proveedor")]
    nombre: STR_NOMBRE


class ProveedorCreateSchema(BaseModel):
    nombre: STR_NOMBRE
