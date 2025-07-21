import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, y_user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)  # Uncomment if you want to auto-create tables

origins = [
    "https://www.google.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(y_user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI on Railway!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# This allows correct deployment via `python -m app.main`
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use $PORT from Railway or fallback to 8000 locally
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

