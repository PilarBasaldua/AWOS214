from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router= APIRouter(tags=['Varios'])

#Endpoint
@router.get("/", tags=["Inicio"]) 
async def bienvenida():
    return {"message": "Bienvenido a mi API"}

@router.get("/HolaMundo", tags=["Bienvenida Asincrona"]) 
async def hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola Mundo FAstAPI" ,
            "estatus" : "200"
            } #formato json

@router.get("/v1/parametroOb/{id}" ,tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id }

@router.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje:":"usuario encontrado", "usuario":usuario}
        return{"mensaje:":"usuario no encontrado", "usuario":id}
    else:
        return{"mensaje:":"No se proporciono id"}
