
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API Sistema de Tickets",
    description="Examen Segundo Parcial",
    version="1.0"
)

security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credentials.username, "soporte")
    passAuth = secrets.compare_digest(credentials.password, "4321")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    return credentials.username


tickets = []

# Modelo
class Ticket(BaseModel):
    id: int = Field(..., gt=0)
    nombre_usuario: str = Field(..., min_length=5)
    descripcion_problema: str = Field(..., min_length=20, max_length=200)
    prioridad: str = Field(..., pattern="^(baja|media|alta)$")
    estado: Optional[str] = "pendiente"


# Bienvenida
@app.get("/")
async def inicio():
    return {"mensaje": "API de Tickets de Soporte"}


# Crear Ticket
@app.post("/tickets", status_code=201)
async def crear_ticket(ticket: Ticket):

    for t in tickets:
        if t["id"] == ticket.id:
            raise HTTPException(
                status_code=400,
                detail="El ticket ya existe"
            )

    tickets.append(ticket.dict())

    return {
        "mensaje": "Ticket creado",
        "ticket": ticket
    }


# Listar Tickets
@app.get("/tickets")
async def listar_tickets():
    return {
        "total": len(tickets),
        "tickets": tickets
    }


# Consultar por ID (protegido)
@app.get("/tickets/{id}")
async def consultar_ticket(id: int, user: str = Depends(verificar_peticion)):

    for t in tickets:
        if t["id"] == id:
            return t

    raise HTTPException(
        status_code=404,
        detail="Ticket no encontrado"
    )


# Cambiar estado (protegido)
@app.put("/tickets/{id}/estado")
async def cambiar_estado(id: int, estado: str, user: str = Depends(verificar_peticion)):

    for t in tickets:
        if t["id"] == id:
            t["estado"] = estado
            return {
                "mensaje": "Estado actualizado",
                "ticket": t
            }

    raise HTTPException(
        status_code=404,
        detail="Ticket no encontrado"
    )


# Eliminar Ticket
@app.delete("/tickets/{id}")
async def eliminar_ticket(id: int):

    for i, t in enumerate(tickets):

        if t["id"] == id:

            if t["estado"] == "resuelto":
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar un ticket resuelto"
                )

            tickets.pop(i)

            return {
                "mensaje": "Ticket eliminado"
            }

    raise HTTPException(
        status_code=404,
        detail="Ticket no encontrado"
    )