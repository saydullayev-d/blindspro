"""
Products repository - Data access layer for products
"""

from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models import BlindsType_, Material, BlindsProduct
from app.repositories.base import BaseRepository


class BlindsTypeRepository(BaseRepository[BlindsType_]):
    """Blinds type data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, BlindsType_)
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[BlindsType_]:
        """Get active blinds types"""
        return self.db.query(BlindsType_).filter(
            BlindsType_.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_name(self, name: str) -> Optional[BlindsType_]:
        """Get blinds type by name"""
        return self.db.query(BlindsType_).filter(BlindsType_.name == name).first()


class MaterialRepository(BaseRepository[Material]):
    """Material data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, Material)
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[Material]:
        """Get active materials"""
        return self.db.query(Material).filter(
            Material.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Material]:
        """Get materials by category"""
        return self.db.query(Material).filter(
            Material.category == category,
            Material.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_name(self, name: str) -> Optional[Material]:
        """Get material by name"""
        return self.db.query(Material).filter(Material.name == name).first()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Material]:
        """Search materials by name or category"""
        search_term = f"%{query}%"
        return self.db.query(Material).filter(
            or_(
                Material.name.ilike(search_term),
                Material.category.ilike(search_term)
            ),
            Material.is_active == True
        ).offset(skip).limit(limit).all()


class BlindsProductRepository(BaseRepository[BlindsProduct]):
    """Blinds product data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, BlindsProduct)
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Get active products"""
        return self.db.query(BlindsProduct).filter(
            BlindsProduct.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_type(self, blinds_type_id: int, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Get products by blinds type"""
        return self.db.query(BlindsProduct).filter(
            BlindsProduct.blinds_type_id == blinds_type_id,
            BlindsProduct.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_material(self, material_id: int, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Get products by material"""
        return self.db.query(BlindsProduct).filter(
            BlindsProduct.material_id == material_id,
            BlindsProduct.is_active == True
        ).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Search products by name or description"""
        search_term = f"%{query}%"
        return self.db.query(BlindsProduct).filter(
            or_(
                BlindsProduct.name.ilike(search_term),
                BlindsProduct.description.ilike(search_term)
            ),
            BlindsProduct.is_active == True
        ).offset(skip).limit(limit).all()
