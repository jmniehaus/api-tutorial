import jwt 
from jwt.exceptions import InvalidTokenError, PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlmodel import select
from .models import TokenData, User
from .database import SessionDep
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
OauthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
OauthBearDep = Annotated[str, Depends(oauth2_scheme)]


def create_access_token(data:dict):
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expires_at})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token 


def verify_access_token(token : str, cred_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise cred_exception

        token_data = TokenData(id=id)

    except PyJWTError:
        raise cred_exception

    return token_data


def get_current_user(token: OauthBearDep, session: SessionDep):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= 'Invalid bearer token.',
        headers = {'WWW-Authenticate' : "Bearer"}
    )

    token = verify_access_token(token, cred_exception=cred_exception)

    user = session.exec(select(User).where(User.id == token.id)).first()

    return user 

UserDep = Annotated[int, Depends(get_current_user)]




