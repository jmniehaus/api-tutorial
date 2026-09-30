from fastapi import status, HTTPException, APIRouter, Depends
from sqlmodel import select, col, func
from typing import Annotated, Optional
from ..oauth2 import UserDep

from ..models import Post, PostCreate, PostPublic, Vote, PostWithVotes
from ..database import SessionDep
###----------



router = APIRouter(prefix = '/posts', tags = ['posts'])



###Posts routes
@router.get("/", response_model = list[PostWithVotes])
def get_posts(session : SessionDep, limit: int = 10, offset = 0, search: Optional[str] = ""):
    posts_stmt = select(Post).where(col(Post.title).contains(search)).limit(limit).offset(offset)
    posts = session.exec(posts_stmt).all()

    n_posts_stmt = select(Post, func.count(Vote.post_id).label('votes')).outerjoin(Vote, Post.id == Vote.post_id).group_by(Post.id)
    n_posts = session.exec(n_posts_stmt).all() 

    return [PostWithVotes(**post.model_dump(), votes=votes) for post, votes in n_posts]



@router.get("/{id}", response_model=PostWithVotes)
def get_post(id: int, session: SessionDep):
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .outerjoin(Vote, Post.id == Vote.post_id)
        .where(Post.id == id)
        .group_by(Post.id)
    )
    row = session.exec(stmt).first()
    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")

    post, votes = row
    return PostWithVotes(**post.model_dump(), votes=votes)


@router.post("/", response_model = PostPublic, status_code = status.HTTP_201_CREATED)
def create_posts(post: PostCreate, session : SessionDep, current_user : UserDep):
    db_post = Post.model_validate(post, update={"owner_id": current_user.id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep,  current_user: UserDep):

    post = session.get(Post, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden.",
        )

    session.delete(post)
    session.commit()


@router.put("/{id}", response_model=PostPublic)
def update_post(post: PostCreate, id: int, session: SessionDep, current_user : UserDep):


    db_post = session.get(Post, id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden.",
        )


    db_post.sqlmodel_update(post.model_dump(exclude_unset=True))
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post