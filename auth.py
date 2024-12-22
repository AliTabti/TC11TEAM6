from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import SessionLocal
import jwt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'y372ye8d4s32e0s32idk4893yf348eu3jsoh238je34jd'
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    hashed_password = pwd_context.hash(create_user_request.password)
    create_user_model = Users(
        email=create_user_request.email,
        password=hashed_password,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authentificate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate User.')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


def authentificate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(email: str, id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
