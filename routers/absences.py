from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Absence
from datetime import date

router = APIRouter()
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ajouter une absence
@router.post("/")
def add_absence(date_absence: date, db: Session = Depends(get_db)):
    new_absence = Absence(date_absence=date_absence)
    db.add(new_absence)
    db.commit()
    db.refresh(new_absence)
    return {"message": "Absence added successfully", "absence": new_absence}

#Récupérer toutes les absences
@router.get("/")
def get_all_absences(db: Session = Depends(get_db)):
    absences = db.query(Absence).all()
    return absences

#Récupérer une absence spécifique par ID
@router.get("/{absence_id}")
def get_absence_by_id(absence_id: int, db: Session = Depends(get_db)):
    absence = db.query(Absence).filter(Absence.id == absence_id).first()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    return absence
