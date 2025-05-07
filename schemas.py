from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoUsuario(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"

class EstadoTarea(str, Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecucion"
    realizada = "Realizada"
    cancelada = "Cancelada"

# Usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioUpdateEstado(BaseModel):
    estado: EstadoUsuario

class UsuarioPremium(BaseModel):
    premium: bool

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    estado: EstadoUsuario
    premium: bool

    class Config:
        orm_mode = True

# Tarea
class TareaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: EstadoTarea = EstadoTarea.pendiente
    usuario_id: int

class TareaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    fecha_modificacion: datetime
    estado: EstadoTarea
    usuario_id: int

    class Config:
        orm_mode = True
