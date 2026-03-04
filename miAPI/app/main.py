from operator import index
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
#Instacia 
app = FastAPI(
    title='Mi primer API',
     description='Pilar Basaldua',
     version='1.0.0'
     )

#seguridad HTTP Basic
security = HTTPBasic()
def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
        userAuth = secrets.compare_digest(credentials.username, "Montserrath Estrada")
        passAuth = secrets.compare_digest(credentials.password, "140320")

        if not (userAuth and passAuth):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no autorizadas"
            )
        return credentials.username    

#TB ficticia 
usuarios=[
    {"id":1,"nombre":"Juan Carlos","edad":23},
    {"id":2,"nombre":"America","edad":20},
    {"id":3,"nombre":"Sofi","edad":19},
]

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max=50, example="Isaac")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")
    

#Endpoint
@app.get("/", tags=["Inicio"]) 
async def bienvenida():
    return {"message": "Bienvenido a mi API"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"]) 
async def hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola Mundo FAstAPI" ,
            "estatus" : "200"
            } #formato json

@app.get("/v1/parametroOb/{id}" ,tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id }

@app.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje:":"usuario encontrado", "usuario":usuario}
        return{"mensaje:":"usuario no encontrado", "usuario":id}
    else:
        return{"mensaje:":"No se proporciono id"}

@app.get("/v1/usuarios/" ,tags=['CRUD HTTP'])
async def leer_usuarios( ):
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/" ,tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios:
        if usr ["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado",
        "Usuario":usuario
    }

@app.put("/v1/usuarios/{id}" ,tags=['CRUD HTTP'])
async def actualizar_usuario(id:int, usuario:dict):
    for i, u in enumerate(usuarios):
        if u["id"] == id:
            usuarios[i] = usuario
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, userAuth: str = Depends(verificar_Peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por: {userAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )