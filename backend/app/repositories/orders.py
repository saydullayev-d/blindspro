from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, date
from app.db.models import Order, OrderItem, OrderStatus, OrderStatusHistory
from app.repositories.base import BaseRepository
from typing import Optional, List


class OrderRepository(BaseRepository[Order]):
    """Order data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, Order)
    
    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        return self.db.query(Order).filter(Order.order_number == order_number).first()
    
    def get_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders for client"""
        return self.db.query(Order).filter(
            Order.client_id == client_id
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status"""
        return self.db.query(Order).filter(
            Order.status == status
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_by_manager(self, manager_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders assigned to manager"""
        return self.db.query(Order).filter(
            Order.manager_id == manager_id
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders created within date range"""
        return self.db.query(Order).filter(
            and_(
                Order.created_at >= datetime.combine(start_date, datetime.min.time()),
                Order.created_at <= datetime.combine(end_date, datetime.max.time())
            )
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    def get_recent(self, limit: int = 20) -> List[Order]:
        """Get recently created orders"""
        return self.db.query(Order).order_by(desc(Order.created_at)).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Search orders by order number or client name"""
        search_term = f"%{query}%"
        return self.db.query(Order).join(Order.client).filter(
            Order.order_number.ilike(search_term) |
            Order.client.name.ilike(search_term)
        ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


class OrderItemRepository(BaseRepository[OrderItem]):
    """Order item data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, OrderItem)
    
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        """Get all items for order"""
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


class OrderStatusHistoryRepository(BaseRepository[OrderStatusHistory]):
    """Order status history data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, OrderStatusHistory)
    
    def get_by_order(self, order_id: int) -> List[OrderStatusHistory]:
        """Get status history for order"""
        return self.db.query(OrderStatusHistory).filter(
            OrderStatusHistory.order_id == order_id
        ).order_by(OrderStatusHistory.changed_at).all()
