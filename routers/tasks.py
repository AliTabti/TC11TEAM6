from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Taches, TaskCreate, EtatTache, User


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Taches(
        date_aff=task.date_aff,
        etat_tache=task.etat_tache,
        task_content=task.task_content
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Lier les utilisateurs à cette tâche
    for user_id in task.user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        user.taches.append(new_task)
    db.commit()
    
    return {"message": "Task created and assigned successfully"}

@router.put("/{task_id}")
def update_task_status(task_id: int, status: EtatTache, db: Session = Depends(get_db)):
    task = db.query(Taches).filter(Taches.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.etat_tache = status
    db.commit()
    return {"message": "Task status updated successfully"}

#Récupérer toutes les tâches
@router.get("/")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Taches).all()
    return tasks

#Récupérer une tâche par ID
@router.get("/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Taches).filter(Taches.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
