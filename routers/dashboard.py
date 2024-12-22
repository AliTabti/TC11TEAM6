from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User, Taches

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    active_tasks = db.query(Taches).filter(Taches.etat_tache == "encours").count()
    return {
        "total_users": total_users,
        "active_tasks": active_tasks
    }

@router.get("/predictions")
def get_predictions():
    # Implémentation d'un modèle prédictif
    return {"message": "Predictions coming soon"}
