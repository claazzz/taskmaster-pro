from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Получить все задачи текущего пользователя"""
    tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return tasks


@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
        task: schemas.TaskCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Создать новую задачу"""
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Получить задачу по ID"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
        task_id: int,
        task_update: schemas.TaskUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Обновить задачу"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # Обновляем только переданные поля
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Удалить задачу"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    db.delete(task)
    db.commit()
    return {"message": "Задача удалена"}