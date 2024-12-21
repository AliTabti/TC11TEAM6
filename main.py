from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base

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
def create_user():
    return "cA VA "

# Endpoint pour obtenir tous les utilisateurs

