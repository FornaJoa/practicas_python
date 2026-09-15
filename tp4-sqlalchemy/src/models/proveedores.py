from database import Base
from sqlalchemy import Column, Integer, String


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
