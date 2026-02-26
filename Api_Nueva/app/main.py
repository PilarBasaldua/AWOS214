from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import date

app = FastAPI(title="API Biblioteca")


class Usuario(BaseModel):
    nombre: str = Field(min_length=2)
    correo: EmailStr


class Libro(BaseModel):
    id: int
    nombre: str = Field(min_length=2, max_length=100)
    autor: str
    anio: int = Field(gt=1450, le=date.today().year)
    paginas: int = Field(gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"


class Prestamo(BaseModel):
    id: int
    libro_id: int
    usuario: Usuario


libros: List[Libro] = []
prestamos: List[Prestamo] = []

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    if not libro.nombre.strip():
        raise HTTPException(400, "El nombre del libro no es válido")

    if any(l.id == libro.id for l in libros):
        raise HTTPException(400, "El libro ya existe")

    libros.append(libro)
    return libro


@app.get("/libros", status_code=status.HTTP_200_OK)
def listar_libros():
    return libros


@app.get("/libros/buscar/{nombre}", status_code=status.HTTP_200_OK)
def buscar_libro(nombre: str):
    return [l for l in libros if nombre.lower() in l.nombre.lower()]


@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):
    libro = next((l for l in libros if l.id == prestamo.libro_id), None)

    if not libro:
        raise HTTPException(400, "El libro no existe")

    if libro.estado == "prestado":
        raise HTTPException(409, "El libro ya está prestado")

    libro.estado = "prestado"
    prestamos.append(prestamo)
    return prestamo


@app.put("/prestamos/devolver/{prestamo_id}", status_code=status.HTTP_200_OK)
def devolver_libro(prestamo_id: int):
    prestamo = next((p for p in prestamos if p.id == prestamo_id), None)

    if not prestamo:
        raise HTTPException(409, "El registro de préstamo no existe")

    libro = next((l for l in libros if l.id == prestamo.libro_id), None)
    if libro:
        libro.estado = "disponible"

    return {"mensaje": "Libro devuelto correctamente"}


@app.delete("/prestamos/{prestamo_id}", status_code=status.HTTP_200_OK)
def eliminar_prestamo(prestamo_id: int):
    prestamo = next((p for p in prestamos if p.id == prestamo_id), None)

    if not prestamo:
        raise HTTPException(409, "El registro de préstamo no existe")

    prestamos.remove(prestamo)
    return {"mensaje": "Préstamo eliminado correctamente"}