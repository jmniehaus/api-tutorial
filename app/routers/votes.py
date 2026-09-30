from fastapi import  status, HTTPException, APIRouter
from ..utils import hash
from ..models import VotePublic, Vote, Post
from ..oauth2 import UserDep
from ..database import SessionDep
from sqlmodel import select

router = APIRouter(prefix = "/votes", tags=['votes'])

###User routes
@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: VotePublic, session : SessionDep, current_user : UserDep):
    post_exists_query = select(Post).where(Post.id == vote.post_id)
    post_exists = session.exec(post_exists_query).first()
    if not post_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = 'post does not exist to vote on.')
    
    vote_query = select(Vote).where(Vote.user_id == current_user.id, Vote.post_id == vote.post_id)
    prior_vote = session.exec(vote_query).first()
    print(prior_vote)
    if vote.vote_dir == 1:
        if prior_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted on this post.")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message":"successfully added vote"}
    else:
        if not prior_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="vote doesn't exist.")
        session.delete(prior_vote)
        session.commit()

        return {"message" : "successfully deleted vote"}
        
