from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from ..oauth2 import create_access_token, OauthFormDep

from ..database import SessionDep
from ..models import User, Token
from ..utils import verify
###-------


router = APIRouter(tags = ['authentication'])

@router.post('/login', response_model = Token)
def login(user_creds: OauthFormDep, session : SessionDep):
    db_user = session.exec(select(User).where(User.email == user_creds.username)).first()

    if not (db_user and verify(user_creds.password, db_user.password)): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password.')

    token = create_access_token(data = {"user_id" : db_user.id})

    return({"access_token" : token, "token_type": "bearer"})
