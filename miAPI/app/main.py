from fastapi import FastAPI
from app.routers import usuarios, varios
#Instacia 
app = FastAPI(
    title='Mi primer API',
     description='Pilar Basaldua',
     version='1.0.0'
     )  

app.include_router(usuarios.router)
app.include_router(varios.router)