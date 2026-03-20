from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mi API con JWT",
    version="2.0"
)

# CONFIGURACION JWT
SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# USUARIO DE PRUEBA
fake_user = {
    "username": "Pilar",
    "password": "060907"
}

# TABLA FICTICIA
usuarios = [
    {"id":1, "nombre":"Juan Carlos", "edad":23},
    {"id":2, "nombre":"Karla", "edad":19},
    {"id":3, "nombre":"America", "edad":20},
]

class UsuarioCreate(BaseModel):
    id:int = Field(..., gt=0)
    nombre:str = Field(..., min_length=3, max_length=50)
    edad:int = Field(..., ge=1, le=120)

# CREAR TOKEN
def crear_token(data:dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# VALIDAR TOKEN
async def verificar_token(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return username


# LOGIN PARA GENERAR TOKEN
@app.post("/token")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):

    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crear_token(
        data={"sub":form_data.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ENDPOINTS

@app.get("/")
async def inicio():
    return {"mensaje":"API con OAuth2 + JWT"}

@app.get("/usuarios")
async def obtener_usuarios():
    return usuarios

@app.post("/usuarios")
async def crear_usuario(usuario:UsuarioCreate):
    usuarios.append(usuario.dict())
    return {"mensaje":"usuario creado"}

# PROTEGIDO CON TOKEN
@app.put("/usuarios/{id}")
async def actualizar_usuario(id:int, usuario:dict, user:str = Depends(verificar_token)):

    for i,u in enumerate(usuarios):
        if u["id"] == id:
            usuarios[i] = usuario
            return {"mensaje":f"usuario actualizado por {user}"}

    raise HTTPException(status_code=404, detail="usuario no encontrado")

# PROTEGIDO CON TOKEN
@app.delete("/usuarios/{id}")
async def eliminar_usuario(id:int, user:str = Depends(verificar_token)):

    for i,u in enumerate(usuarios):
        if u["id"] == id:
            usuarios.pop(i)
            return {"mensaje":f"usuario eliminado por {user}"}

    raise HTTPException(status_code=404, detail="usuario no encontrado")