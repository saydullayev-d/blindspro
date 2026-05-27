from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from app.db.models import (
    UserRole, OrderStatus, BlindsType, ControlType, InteractionStatus
)


# ==================== Auth Schemas ====================
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = None


class UserLoginRequest(BaseModel):
    username: str
    password: str


# ==================== User Schemas ====================
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.MANAGER
    is_active: bool = True
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Client Schemas ====================
class ClientNoteBase(BaseModel):
    content: str = Field(..., min_length=1)


class ClientNoteCreate(ClientNoteBase):
    pass


class ClientNoteResponse(ClientNoteBase):
    id: int
    client_id: int
    created_by: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    interaction_status: InteractionStatus = InteractionStatus.NEW
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    manager_id: Optional[int] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    interaction_status: Optional[InteractionStatus] = None
    notes: Optional[str] = None


class ClientResponse(ClientBase):
    id: int
    manager_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    client_notes: List[ClientNoteResponse] = []

    class Config:
        from_attributes = True


class ClientDetailResponse(ClientResponse):
    manager: Optional[UserResponse] = None
    orders: List['OrderResponse'] = []


# ==================== Product Schemas ====================
class MaterialBase(BaseModel):
    name: str = Field(..., min_length=1)
    category: str
    description: Optional[str] = None
    color: Optional[str] = None
    price_per_unit: float = Field(..., gt=0)
    unit: str = "piece"
    stock_quantity: int = 0
    min_stock_level: int = 10
    supplier: Optional[str] = None
    is_active: bool = True


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    price_per_unit: Optional[float] = None
    unit: Optional[str] = None
    stock_quantity: Optional[int] = None
    min_stock_level: Optional[int] = None
    supplier: Optional[str] = None
    is_active: Optional[bool] = None


class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductConfigurationBase(BaseModel):
    config_name: str
    config_value: str
    price_modifier: float = 0


class ProductConfigurationResponse(ProductConfigurationBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class BlindsProductBase(BaseModel):
    blinds_type_id: int
    material_id: int
    control_type: ControlType
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    is_active: bool = True


class BlindsProductCreate(BlindsProductBase):
    pass


class BlindsProductResponse(BlindsProductBase):
    id: int
    created_at: datetime
    material: Optional[MaterialResponse] = None
    configurations: List[ProductConfigurationResponse] = []

    class Config:
        from_attributes = True


# ==================== Order Schemas ====================
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    width_mm: int = Field(..., gt=0)
    height_mm: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    custom_options: Optional[str] = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    total_price: float
    product: Optional[BlindsProductResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderStatusHistoryResponse(BaseModel):
    id: int
    old_status: Optional[OrderStatus]
    new_status: OrderStatus
    changed_by: Optional[UserResponse]
    notes: Optional[str]
    changed_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    discount_percentage: float = Field(default=0, ge=0, le=100)
    notes: Optional[str] = None
    measurement_notes: Optional[str] = None
    delivery_address: Optional[str] = None
    required_delivery_date: Optional[date] = None


class OrderCreate(OrderBase):
    client_id: int
    manager_id: Optional[int] = None
    order_items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = None
    measurement_notes: Optional[str] = None
    delivery_address: Optional[str] = None
    required_delivery_date: Optional[date] = None


class OrderResponse(OrderBase):
    id: int
    order_number: str
    client_id: int
    manager_id: Optional[int]
    status: OrderStatus
    total_price: float
    final_price: float
    actual_delivery_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    client: ClientResponse
    manager: Optional[UserResponse]
    status_history: List[OrderStatusHistoryResponse] = []


# ==================== Production Schemas ====================
class ProductionTaskBase(BaseModel):
    order_id: int
    assigned_to_id: Optional[int] = None
    status: str = "pending"
    priority: int = 0
    estimated_hours: Optional[float] = None
    notes: Optional[str] = None


class ProductionTaskCreate(ProductionTaskBase):
    pass


class ProductionTaskUpdate(BaseModel):
    assigned_to_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    notes: Optional[str] = None


class ProductionTaskResponse(ProductionTaskBase):
    id: int
    task_number: str
    actual_hours: Optional[float]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    order: Optional[OrderResponse]
    assigned_to: Optional[UserResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Warehouse Schemas ====================
class WarehouseMovementBase(BaseModel):
    material_id: int
    movement_type: str  # "in", "out", "adjustment"
    quantity: int = Field(..., ne=0)
    reason: str
    reference_id: Optional[int] = None
    notes: Optional[str] = None


class WarehouseMovementCreate(WarehouseMovementBase):
    pass


class WarehouseMovementResponse(WarehouseMovementBase):
    id: int
    created_by_id: Optional[int]
    created_at: datetime
    material: Optional[MaterialResponse]

    class Config:
        from_attributes = True


class MaterialReservationBase(BaseModel):
    material_id: int
    quantity: int = Field(..., gt=0)


class MaterialReservationResponse(MaterialReservationBase):
    id: int
    order_id: int
    reserved_at: datetime
    used_at: Optional[datetime]
    is_used: bool

    class Config:
        from_attributes = True


# ==================== Schedule Schemas ====================
class ScheduleItemBase(BaseModel):
    order_id: int
    installer_id: int
    task_type: str  # "measurement", "installation"
    scheduled_date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class ScheduleItemCreate(ScheduleItemBase):
    pass


class ScheduleItemUpdate(BaseModel):
    task_type: Optional[str] = None
    scheduled_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class ScheduleItemResponse(ScheduleItemBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    order: Optional[OrderResponse]
    installer: Optional[UserResponse]

    class Config:
        from_attributes = True


# ==================== Configurator Schemas ====================
class BlindConfigurationRequest(BaseModel):
    """Request for configurator pricing calculation"""
    blinds_type: str
    material_id: int
    control_type: str
    width_mm: int = Field(..., gt=0)
    height_mm: int = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)
    custom_options: Optional[dict] = None


class BlindConfigurationResponse(BaseModel):
    """Response with configured blind details and pricing"""
    blinds_type: str
    material: MaterialResponse
    control_type: str
    width_mm: int
    height_mm: int
    quantity: int
    unit_price: float
    total_price: float
    area_sqm: float
    custom_options: Optional[dict]


# ==================== Pagination Schemas ====================
class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: str = "desc"


class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List


# ==================== Error Schemas ====================
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
