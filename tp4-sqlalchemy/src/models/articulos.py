from database import Base
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String


class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Float)
    modelo = Column(String)
    activo = Column(Boolean)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
