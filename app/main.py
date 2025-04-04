from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.routers import users, tasks
from app.dependencies import get_db
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware 
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users.router)
app.include_router(tasks.router)

# Test DB connection route
@app.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")) 
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "details": str(e)}
    
@app.get("/")
def read_root():
    return {"message": "Hello World"}