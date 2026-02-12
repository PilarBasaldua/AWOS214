#Importaciones
from fastapi import FastAPI
import asyncio 
from typing import Optional 

#Instacia 
app = FastAPI(
    title='Mi primer API',
     description='Pilar Basaldua',
     version='1.0.0'
     )
#TB ficticia 
usuarios=[
    {"id":1,"nombre":"Juan Carlos","edad":23},
    {"id":2,"nombre":"America","edad":20},
    {"id":3,"nombre":"Sofi","edad":19},
]

#Endpoinst
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "¡Bienvenido de mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) #Simulacion de una peticion
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus": "200"
    }

@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario": id}

@app.get("/v1/usuarios/", tags=['Parametro opcional'])
async def consultaTodos(id: Optional[int]= None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id: 
                return{"mensaje":"usuario encontrado", "usuario": usuario}
        return{"mensaje":"usuario no encontrado", "usuario": id}
    else:
        return{"mensaje":"No se proporciono id"}
