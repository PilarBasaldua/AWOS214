from fastapi import APIRouter, FastAPI, status, HTTPException, Depends
from app.models.usuario import usuario_create
from app.data.database import usuarios 
from app.security.auth import verificar_Peticion

router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)


@router.get("/")
async def leer_usuarios( ):
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
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

@router.put("/{id}")
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

@router.delete("/{id}")
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