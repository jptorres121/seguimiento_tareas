from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()


# Enums para estados
class EstadoTarea(str, enum.Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecucion"
    realizada = "Realizada"
    cancelada = "Cancelada"


class EstadoUsuario(str, enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"


# Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    estado = Column(Enum(EstadoUsuario), default=EstadoUsuario.activo)
    premium = Column(Boolean, default=False)

    tareas = relationship("Tarea", back_populates="usuario")


# Modelo Tarea
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(Enum(EstadoTarea), default=EstadoTarea.pendiente)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="tareas")
