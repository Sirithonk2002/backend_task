# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app import models, schemas, auth
# from app.database import SessionLocal
# from app.dependencies import get_db
# from fastapi.security import OAuth2PasswordBearer
# from dotenv import load_dotenv
# import os

# # โหลดค่าจากไฟล์ .env
# load_dotenv()

# # ดึงค่า SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES จากไฟล์ .env
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# router = APIRouter(prefix="/users", tags=["users"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# @router.post("/register")
# def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(models.user).filter(models.user.username == user_data.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     hashed_pwd = auth.hash_password(user_data.password)
#     new_user = models.User(
#         username=user_data.username,
#         password=hashed_pwd  
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"id": new_user.id, "username": new_user.username}


# @router.post("/login")
# def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(models.user).filter(models.user.username == credentials.username).first()
#     if not user or not auth.verify_password(credentials.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     access_token = auth.create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users")
# async def get_users(db: Session = Depends(get_db)):
#     users = db.query(models.user).all()
#     return users


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     payload = auth.decode_access_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.query(models.user).filter(models.user.username == payload.get("sub")).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.get("/me", response_model=schemas.UserResponse)
# def get_me(current_user: models.User = Depends(get_current_user)):
#     return current_user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.dependencies import get_db
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/register")
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pwd = auth.hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        password=hashed_pwd  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}

@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or not auth.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
