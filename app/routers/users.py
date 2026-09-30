from fastapi import  status, HTTPException, APIRouter
from ..database import SessionDep
from ..models import User, UserCreate, UserPublic
from ..utils import hash


router = APIRouter(prefix = "/users", tags=['users'])

###User routes
@router.post("/", response_model = UserPublic, status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate, session : SessionDep):
    hashed_password = hash(user.password)
    user.password = hashed_password
    db_user = User.model_validate(user) 
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/{id}", response_model = UserPublic)
def get_user(id:int, session:SessionDep):
    db_user = session.get(User, id)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    return db_user


