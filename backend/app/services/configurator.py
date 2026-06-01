"""
Configurator service
Business logic for blind configuration and pricing
"""

from sqlalchemy.orm import Session
from app.db.schemas import BlindConfigurationRequest, BlindConfigurationResponse
from app.repositories.products import MaterialRepository, BlindsProductRepository
from app.core.constants import PRICE_MULTIPLIERS, CONTROL_TYPE_MULTIPLIERS, BASE_PRICE_PER_SQM
from app.core.exceptions import ValidationError


class ConfiguratorService:
    """Service for blind configuration calculations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.material_repo = MaterialRepository(db)
        self.product_repo = BlindsProductRepository(db)
    
    def calculate_configuration(self, config: BlindConfigurationRequest) -> BlindConfigurationResponse:
        """
        Calculate pricing for blind configuration
        
        Pricing formula:
        unit_price = base_price * area_sqm * type_multiplier * material_price * control_multiplier
        total_price = unit_price * quantity
        """
        
        # Validate material exists
        material = self.material_repo.get_by_id(config.material_id)
        if not material or not material.is_active:
            raise ValidationError(f"Material with id {config.material_id} not found or inactive")
        
        # Validate dimensions
        if config.width_mm <= 0 or config.height_mm <= 0:
            raise ValidationError("Width and height must be greater than 0")
        
        # Calculate area in square meters
        area_sqm = (config.width_mm * config.height_mm) / 1_000_000
        
        # Get multipliers
        type_multiplier = PRICE_MULTIPLIERS.get(config.blinds_type, 1.0)
        control_multiplier = CONTROL_TYPE_MULTIPLIERS.get(config.control_type, 1.0)
        
        # Calculate unit price
        unit_price = (
            BASE_PRICE_PER_SQM 
            * area_sqm 
            * type_multiplier 
            * control_multiplier
            * (material.price_per_unit or 1.0)
        )
        
        # Calculate total price
        total_price = unit_price * config.quantity
        
        return BlindConfigurationResponse(
            blinds_type=config.blinds_type,
            material=material,
            control_type=config.control_type,
            width_mm=config.width_mm,
            height_mm=config.height_mm,
            quantity=config.quantity,
            unit_price=round(unit_price, 2),
            total_price=round(total_price, 2),
            area_sqm=round(area_sqm, 4),
            custom_options=config.custom_options,
        )
