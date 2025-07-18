from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .import models
from .database import engine
from .routers import post,y_user,auth,vote
from .config import settings



#models.Base.metadata.create_all(bind=engine) # This line is used to create the tables in the database if they do not exist

origins=["https://www.google.com"]

app=FastAPI()

app.add_middleware( CORSMiddleware
                   , allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"], )

app.include_router(post.router)
app.include_router(y_user.router)
app.include_router(auth.router)
app.include_router(vote.router)



