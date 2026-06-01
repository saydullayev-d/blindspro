"""
Orders repository - Data access layer for orders
"""

from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models import Order, OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Order data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, Order)
    
    def get_by_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        return self.db.query(Order).filter(Order.order_number == order_number).first()
    
    def get_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by client"""
        return self.db.query(Order).filter(
            Order.client_id == client_id
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status"""
        return self.db.query(Order).filter(
            Order.status == status
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_recent(self, limit: int = 20) -> List[Order]:
        """Get recent orders"""
        return self.db.query(Order).order_by(
            desc(Order.created_at)
        ).limit(limit).all()


class OrderItemRepository(BaseRepository[OrderItem]):
    """Order item data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, OrderItem)
    
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        """Get all items for an order"""
        return self.db.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
