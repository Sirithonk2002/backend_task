from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.dependencies import get_db
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from datetime import date

router = APIRouter(prefix="/tasks", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username: str = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#CREATE
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        new_task = models.Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            start_date=task_data.start_date,
            end_date=task_data.end_date,
            user_id=current_user.id
        )
        if task_data.assignee_ids:
            assignees = db.query(models.User).filter(models.User.id.in_(task_data.assignee_ids)).all()
            if len(assignees) != len(task_data.assignee_ids):
                raise HTTPException(status_code=400, detail="Some assignees not found")
            new_task.assignees = assignees

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except Exception as e:
        print(f"Error while creating task: {e}")  
        raise HTTPException(status_code=500, detail="Error creating task: " + str(e))

#READ 
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
    status: Optional[schemas.TaskStatus] = None,
    priority: Optional[schemas.TaskPriority] = None,
    start_from: Optional[date] = None,
    end_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)
    
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if start_from:
        query = query.filter(models.Task.start_date >= start_from)
    if end_to:
        query = query.filter(models.Task.end_date <= end_to)

    return query.all()

#UPDATE
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    update_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id and current_user not in task.assignees:
        raise HTTPException(status_code=403, detail="You do not have access to this task")

    for field, value in update_data.dict(exclude_unset=True, exclude={"assignee_ids"}).items():
        setattr(task, field, value)

    if update_data.assignee_ids is not None:
        assignees = db.query(models.User).filter(models.User.id.in_(update_data.assignee_ids)).all()
        task.assignees = assignees

    db.commit()
    db.refresh(task)
    return task

#DELETE
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
