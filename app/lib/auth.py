from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
import os
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError


# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes="bcrypt")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_TIME = 60


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=EXPIRY_TIME)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return email