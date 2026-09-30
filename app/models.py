from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from sqlalchemy import DateTime, func, true
from pydantic import EmailStr, BaseModel
from typing import Optional, Annotated


###Posts
class PostBase(SQLModel):
    title : str = Field(nullable = False)
    content : str = Field(nullable = False)
    published : bool = Field(
        default = True, 
        nullable = False, 
        sa_column_kwargs = {"server_default": true()}
    )


class Post(PostBase, table = True):
    __tablename__ = 'posts'

    id : int | None = Field(default = None, primary_key = True)
    created_at: datetime | None = Field(
        default = None,
        nullable = False,
        sa_type = DateTime(timezone=True),
        sa_column_kwargs = {"server_default": func.now()}
    )
    owner_id : int = Field(foreign_key='users.id', nullable = False, ondelete='CASCADE')
    owner : 'User' = Relationship()

class PostWithVotes(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    votes: int



class PostCreate(PostBase):
    pass



###Users
class UserBase(SQLModel):
    email : EmailStr = Field(nullable = False, unique = True)
    password : str = Field(nullable =False)


class User(SQLModel, table = True): 
    __tablename__ = "users"

    id : int | None = Field(default = None, primary_key = True)
    email : EmailStr = Field(nullable = False, unique = True)
    password : str = Field(nullable =False)
    created_at: datetime | None = Field(
        default = None,
        nullable = False,
        sa_type = DateTime(timezone=True),
        sa_column_kwargs = {"server_default": func.now()}
    )


class UserCreate(UserBase):
    pass


class UserPublic(SQLModel):
    id : int 
    email : EmailStr
    created_at: datetime | None = Field(
        default = None,
        nullable = False,
        sa_type = DateTime(timezone=True),
        sa_column_kwargs = {"server_default": func.now()}
    )

class PostPublic(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner: UserPublic


class Token(BaseModel):
    access_token: str
    token_type : str 


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(SQLModel, table=True):
    __tablename__='votes'

    user_id: int = Field(foreign_key='users.id', nullable=False, ondelete='CASCADE', primary_key=True)
    post_id: int = Field(foreign_key='posts.id', nullable=False, ondelete='CASCADE', primary_key=True)


class VotePublic(SQLModel):
        post_id: int 
        vote_dir: Annotated[int, Field(ge=0, le=1)]

