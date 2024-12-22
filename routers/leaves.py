from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Conge, EtatConge
from datetime import date, time, datetime



router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def request_leave(cause: str, date_demande: date, date_fin: date, db: Session = Depends(get_db)):
    new_leave = Conge(
        cause=cause,
        etat=EtatConge.attente,
        date_demande=date_demande,
        date_fin=date_fin
    )
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return {"message": "Leave requested successfully"}

@router.put("/{leave_id}/validate")
def validate_leave(leave_id: int, status: EtatConge, db: Session = Depends(get_db)):
    leave = db.query(Conge).filter(Conge.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.etat = status
    db.commit()
    return {"message": "Leave status updated"}
