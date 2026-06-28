from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from . import models
from .database import get_db
from .auth import get_current_user

router = APIRouter()


@router.get("/summary")
def get_analytics(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Получить сводную статистику по задачам"""

    # Общее количество задач
    total_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).count()

    # Активные задачи
    active_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == "active"
    ).count()

    # Выполненные задачи
    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == "completed"
    ).count()

    # Просроченные задачи (если есть due_date и она меньше сегодня)
    today = datetime.now().date()
    overdue_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.status != "completed",
        func.date(models.Task.due_date) < today
    ).count()

    # Приоритеты
    high_priority = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.priority == "high",
        models.Task.status != "completed"
    ).count()

    return {
        "total": total_tasks,
        "active": active_tasks,
        "completed": completed_tasks,
        "overdue": overdue_tasks,
        "high_priority_active": high_priority,
        "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
    }


@router.get("/activity")
def get_activity(
        days: int = 7,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Получить активность по дням (сколько задач создано за последние N дней)"""

    start_date = datetime.now() - timedelta(days=days)

    results = db.query(
        func.date(models.Task.created_at).label("date"),
        func.count(models.Task.id).label("count")
    ).filter(
        models.Task.user_id == current_user.id,
        models.Task.created_at >= start_date
    ).group_by(func.date(models.Task.created_at)).all()

    return [
        {"date": str(r.date), "count": r.count} for r in results
    ]