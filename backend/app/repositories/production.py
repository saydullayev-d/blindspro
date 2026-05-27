from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from app.db.models import ProductionTask
from app.repositories.base import BaseRepository
from typing import Optional, List


class ProductionTaskRepository(BaseRepository[ProductionTask]):
    """Production task data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, ProductionTask)
    
    def get_by_order(self, order_id: int) -> List[ProductionTask]:
        """Get all tasks for order"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.order_id == order_id
        ).order_by(desc(ProductionTask.priority), ProductionTask.created_at).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get tasks by status"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.status == status
        ).order_by(desc(ProductionTask.priority), ProductionTask.created_at).offset(skip).limit(limit).all()
    
    def get_assigned_to(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get tasks assigned to user"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.assigned_to_id == user_id
        ).order_by(desc(ProductionTask.priority), ProductionTask.created_at).offset(skip).limit(limit).all()
    
    def get_pending(self, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get pending tasks"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.status == "pending"
        ).order_by(desc(ProductionTask.priority), ProductionTask.created_at).offset(skip).limit(limit).all()
    
    def get_in_progress(self, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get in-progress tasks"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.status == "in_progress"
        ).order_by(ProductionTask.created_at).offset(skip).limit(limit).all()
    
    def get_by_priority(self, priority: int, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get tasks by priority level"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.priority == priority
        ).order_by(ProductionTask.created_at).offset(skip).limit(limit).all()
    
    def get_high_priority(self, skip: int = 0, limit: int = 100) -> List[ProductionTask]:
        """Get high priority tasks (priority >= 1)"""
        return self.db.query(ProductionTask).filter(
            ProductionTask.priority >= 1
        ).order_by(desc(ProductionTask.priority), ProductionTask.created_at).offset(skip).limit(limit).all()
