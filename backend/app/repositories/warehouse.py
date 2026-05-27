from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.db.models import WarehouseMovement, MaterialReservation
from app.repositories.base import BaseRepository
from typing import Optional, List


class WarehouseMovementRepository(BaseRepository[WarehouseMovement]):
    """Warehouse movement data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, WarehouseMovement)
    
    def get_by_material(self, material_id: int, skip: int = 0, limit: int = 100) -> List[WarehouseMovement]:
        """Get all movements for material"""
        return self.db.query(WarehouseMovement).filter(
            WarehouseMovement.material_id == material_id
        ).order_by(desc(WarehouseMovement.created_at)).offset(skip).limit(limit).all()
    
    def get_by_type(self, movement_type: str, skip: int = 0, limit: int = 100) -> List[WarehouseMovement]:
        """Get movements by type (in, out, adjustment)"""
        return self.db.query(WarehouseMovement).filter(
            WarehouseMovement.movement_type == movement_type
        ).order_by(desc(WarehouseMovement.created_at)).offset(skip).limit(limit).all()
    
    def get_recent(self, limit: int = 50) -> List[WarehouseMovement]:
        """Get recent movements"""
        return self.db.query(WarehouseMovement).order_by(
            desc(WarehouseMovement.created_at)
        ).limit(limit).all()


class MaterialReservationRepository(BaseRepository[MaterialReservation]):
    """Material reservation data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, MaterialReservation)
    
    def get_by_order(self, order_id: int) -> List[MaterialReservation]:
        """Get all reservations for order"""
        return self.db.query(MaterialReservation).filter(
            MaterialReservation.order_id == order_id
        ).all()
    
    def get_by_material(self, material_id: int) -> List[MaterialReservation]:
        """Get all reservations for material"""
        return self.db.query(MaterialReservation).filter(
            MaterialReservation.material_id == material_id
        ).all()
    
    def get_unused_for_order(self, order_id: int) -> List[MaterialReservation]:
        """Get unused reservations for order"""
        return self.db.query(MaterialReservation).filter(
            MaterialReservation.order_id == order_id,
            MaterialReservation.is_used == False
        ).all()
