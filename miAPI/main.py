#Importaciones
from fastapi import FastAPI
import asyncio 

#Instacia 
app = FastAPI()

#Endpoinst
@app.get("/")
async def bienvenida():
    return {"mensaje": "¡Bienvenido de mi API!"}

@app.get("/HolaMundo")
async def hola():
    await asyncio.sleep(4) #Simulacion de una peticion
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus": "200"
    }