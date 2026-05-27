from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.db.models import BlindsProduct, Material, BlindsType_, ControlType, ProductConfiguration
from app.repositories.base import BaseRepository
from typing import Optional, List


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
            BlindsProduct.blinds_type_id == blinds_type_id
        ).offset(skip).limit(limit).all()
    
    def get_by_material(self, material_id: int, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Get products by material"""
        return self.db.query(BlindsProduct).filter(
            BlindsProduct.material_id == material_id
        ).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[BlindsProduct]:
        """Search products by name or description"""
        search_term = f"%{query}%"
        return self.db.query(BlindsProduct).filter(
            or_(
                BlindsProduct.name.ilike(search_term),
                BlindsProduct.description.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()


class MaterialRepository(BaseRepository[Material]):
    """Material data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, Material)
    
    def get_by_name(self, name: str) -> Optional[Material]:
        """Get material by name"""
        return self.db.query(Material).filter(Material.name == name).first()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Material]:
        """Get materials by category"""
        return self.db.query(Material).filter(
            Material.category == category
        ).offset(skip).limit(limit).all()
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[Material]:
        """Get active materials"""
        return self.db.query(Material).filter(
            Material.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_low_stock(self) -> List[Material]:
        """Get materials with low stock"""
        return self.db.query(Material).filter(
            Material.stock_quantity <= Material.min_stock_level
        ).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Material]:
        """Search materials by name, color, or category"""
        search_term = f"%{query}%"
        return self.db.query(Material).filter(
            or_(
                Material.name.ilike(search_term),
                Material.color.ilike(search_term),
                Material.category.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()


class BlindsTypeRepository(BaseRepository[BlindsType_]):
    """Blinds type data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, BlindsType_)
    
    def get_by_name(self, name: str) -> Optional[BlindsType_]:
        """Get blinds type by name"""
        return self.db.query(BlindsType_).filter(BlindsType_.name == name).first()
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[BlindsType_]:
        """Get active blinds types"""
        return self.db.query(BlindsType_).filter(
            BlindsType_.is_active == True
        ).offset(skip).limit(limit).all()


class ProductConfigurationRepository(BaseRepository[ProductConfiguration]):
    """Product configuration data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, ProductConfiguration)
    
    def get_by_product(self, product_id: int) -> List[ProductConfiguration]:
        """Get configurations for product"""
        return self.db.query(ProductConfiguration).filter(
            ProductConfiguration.product_id == product_id
        ).all()
