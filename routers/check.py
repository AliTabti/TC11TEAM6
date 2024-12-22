from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Check, CheckCreate


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/checkin")
def check_in(check: CheckCreate, db: Session = Depends(get_db)):
    new_check = Check(
        date_checkin=check.date_checkin,
        heure_checkin=check.heure_checkin,
        heure_checkout=check.heure_checkout
    )
    db.add(new_check)
    db.commit()
    db.refresh(new_check)
    return {"message": "Check-in successful"}

@router.put("/checkout/{check_id}")
def check_out(check_id: int, checkout_time: str, db: Session = Depends(get_db)):
    check = db.query(Check).filter(Check.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Check-in record not found")
    check.heure_checkout = checkout_time
    db.commit()
    return {"message": "Check-out successful"}
