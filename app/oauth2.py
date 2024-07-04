from jose import JWTError, jwt
from datetime import datetime, timedelta
from. import schemas,database,models
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

#screet_key
#Algorithm
#expiration_time

# one can provide secret key with " openssl rand -hex 32 " command
SECRET_KEY = "6aad8216aa1e5c7de0fde3150b91b82a9d8362f38df561b6af550eb4dcff67d8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:
    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authanticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    db.query(models.User).filter(models.User.id == token.id).first()
    return user