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





















"""
# Hash password function
def hash_password(password: str):
    return pwd_context.hash(password)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Create a new user
@app.post("/admin/create")
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get a user by ID
@app.get("/admin/{user_id}")
def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


# Update a user
@app.put("/user/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete a user
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(db_user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}


@app.post("/checkin")
def check_in(check: CheckCreate, db: Session = Depends(get_db)):
    new_check = Check(
        date_checkin=check.date_checkin,
        heure_checkin=check.heure_checkin,
        heure_checkout=check.heure_checkout
    )
    db.add(new_check)
    db.commit()
    db.refresh(new_check)
    return new_check


# Get check-in/check-out hours for an employee
@app.get("/check/{check_id}")
def get_check(check_id: int, db: Session = Depends(get_db)):
    check = db.query(Check).filter(Check.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Enregistrement non trouvé")
    return check


# Create a task
@app.post("/tasks/create")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Taches(
        date_aff=task.date_aff,
        etat_tache=task.etat_tache,
        task_content=task.task_content
    )

    users = db.query(User).filter(User.id.in_(task.user_ids)).all()

    if len(users) != len(task.user_ids):
        raise HTTPException(status_code=404, detail="Un ou plusieurs utilisateurs non trouvés")

    new_task.users.extend(users)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Update the status of a task
@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, etat: EtatTache, db: Session = Depends(get_db)):
    task = db.query(Taches).filter(Taches.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    task.etat_tache = etat
    db.commit()
    db.refresh(task)
    return task

"""