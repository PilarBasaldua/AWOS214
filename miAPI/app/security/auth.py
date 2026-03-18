from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


#seguridad HTTP Basic
security = HTTPBasic()
def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
        userAuth = secrets.compare_digest(credentials.username, " Pilar")
        passAuth = secrets.compare_digest(credentials.password, "123456")

        if not (userAuth and passAuth):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no autorizadas"
            )
        return credentials.username  