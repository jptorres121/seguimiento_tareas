from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST Adicionar usuario
@app.post("/usuarios/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# GET Todos los usuarios
@app.get("/usuarios/", response_model=list[schemas.UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

# GET Un solo usuario
@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# PUT Actualizar estado
@app.put("/usuarios/{usuario_id}/estado", response_model=schemas.UsuarioOut)
def actualizar_estado(usuario_id: int, estado: schemas.UsuarioUpdateEstado, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.estado = estado.estado
    db.commit()
    db.refresh(usuario)
    return usuario

# PUT Hacer usuario PREMIUM
@app.put("/usuarios/{usuario_id}/premium", response_model=schemas.UsuarioOut)
def hacer_premium(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.premium = True
    db.commit()
    db.refresh(usuario)
    return usuario

# GET Usuarios inactivos
@app.get("/usuarios/inactivos", response_model=list[schemas.UsuarioOut])
def obtener_usuarios_inactivos(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.estado == "Inactivo").all()

# GET Usuarios premium e inactivos
@app.get("/usuarios/premium-inactivos", response_model=list[schemas.UsuarioOut])
def obtener_usuarios_premium_inactivos(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(
        models.Usuario.estado == "Inactivo",
        models.Usuario.premium == True
    ).all()
