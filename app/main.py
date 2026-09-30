from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from .database import create_db_and_tables
#from contextlib import asynccontextmanager
from .routers import posts, users, auth, votes



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield


#app = FastAPI(lifespan = lifespan)
app = FastAPI()

origins = ['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message" : "hello world"}

