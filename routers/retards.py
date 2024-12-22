from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Retard
from datetime import date, time

router = APIRouter()
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ajouter un retard
@router.post("/")
def add_retard(date_retard: date, heure_retard: time, db: Session = Depends(get_db)):
    new_retard = Retard(date_retard=date_retard, heure_retard=heure_retard)
    db.add(new_retard)
    db.commit()
    db.refresh(new_retard)
    return {"message": "Retard added successfully", "retard": new_retard}

#Récupérer tous les retards
@router.get("/")
def get_all_retards(db: Session = Depends(get_db)):
    retards = db.query(Retard).all()
    return retards

#Récupérer un retard spécifique par ID
@router.get("/{retard_id}")
def get_retard_by_id(retard_id: int, db: Session = Depends(get_db)):
    retard = db.query(Retard).filter(Retard.id == retard_id).first()
    if not retard:
        raise HTTPException(status_code=404, detail="Retard not found")
    return retard
