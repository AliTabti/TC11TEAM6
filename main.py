from fastapi import FastAPI, Depends, HTTPException, Request, Response
from typing import Annotated
from sqlalchemy.orm import Session
import database as database
from database import SessionLocal, engine, Base

from models import User, UserCreate, Check, CheckCreate, TaskCreate, Taches, EtatTache
from sqlalchemy.orm import relationship
from routers import auth, check, tasks, leaves, dashboard, absences, retards


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(check.router, prefix="/check", tags=["Check-in/Check-out"])
app.include_router(tasks.router, prefix="/tasks", tags=["Gestion des Tâches"])
app.include_router(leaves.router, prefix="/leaves", tags=["Gestion des Congés"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(absences.router, prefix="/absences", tags=["Gestion des Absences"])
app.include_router(retards.router, prefix="/retards", tags=["Gestion des Retards"])