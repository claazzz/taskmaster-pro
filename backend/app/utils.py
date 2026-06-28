import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

def format_datetime(dt: datetime) -> str:
    """Форматирует дату для вывода"""
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return ""

def log_request(endpoint: str, data: Dict[str, Any]):
    """Логирует входящий запрос"""
    logger.info(f"Request to {endpoint}: {data}")

def validate_priority(priority: str) -> bool:
    """Проверяет, что приоритет корректен"""
    return priority in ["low", "medium", "high"]

def validate_status(status: str) -> bool:
    """Проверяет, что статус корректен"""
    return status in ["active", "completed", "archived"]