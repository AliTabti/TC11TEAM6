from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import test

# Créer toutes les tables au démarrage

app = FastAPI()

# Fonction de dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pour créer un utilisateur
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = test(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Endpoint pour obtenir tous les utilisateurs
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(test).all()
