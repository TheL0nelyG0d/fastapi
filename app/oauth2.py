from jose import JWTError, jwt
from datetime import datetime, timedelta

#screet_key
#Algorithm
#expiration_time

# one can provide secret key with " openssl rand -hex 32 " command
SECRET_KEY = "6aad8216aa1e5c7de0fde3150b91b82a9d8362f38df561b6af550eb4dcff67d8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
