from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    ForeignKey, Text, Enum, Table, UniqueConstraint,
    Numeric, Date
)
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    PRODUCTION = "production"
    INSTALLER = "installer"


class OrderStatus(str, enum.Enum):
    """Order status workflow"""
    NEW = "new"
    PROCESSING = "processing"
    PRODUCTION = "production"
    READY = "ready"
    DELIVERED = "delivered"
    INSTALLED = "installed"
    CANCELLED = "cancelled"


class BlindsType(str, enum.Enum):
    """Types of blinds"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    ROLLER = "roller"
    PANEL = "panel"
    MOTORIZED = "motorized"


class ControlType(str, enum.Enum):
    """Control mechanism types"""
    MANUAL = "manual"
    MOTOR = "motor"
    SMART = "smart"
    CHAIN = "chain"


class InteractionStatus(str, enum.Enum):
    """Client interaction statuses"""
    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NEGOTIATING = "negotiating"
    CUSTOMER = "customer"
    INACTIVE = "inactive"


# ==================== Users ====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.MANAGER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    clients = relationship("Client", back_populates="manager")
    orders = relationship("Order", back_populates="manager")
    notes = relationship("ClientNote", back_populates="created_by")
    production_tasks = relationship("ProductionTask", back_populates="assigned_to")
    schedule_items = relationship("ScheduleItem", back_populates="installer")


# ==================== Clients (CRM) ====================
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    company_name = Column(String(255), nullable=True)
    contact_person = Column(String(255), nullable=True)
    interaction_status = Column(Enum(InteractionStatus), default=InteractionStatus.NEW, nullable=False)
    notes = Column(Text, nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    manager = relationship("User", back_populates="clients")
    orders = relationship("Order", back_populates="client")
    client_notes = relationship("ClientNote", back_populates="client", cascade="all, delete-orphan")


class ClientNote(Base):
    __tablename__ = "client_notes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="client_notes")
    created_by = relationship("User", back_populates="notes")


# ==================== Products & Materials ====================
class BlindsType_(Base):
    __tablename__ = "blinds_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    blinds_products = relationship("BlindsProduct", back_populates="blinds_type")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(50), nullable=True)
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), default="piece", nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    min_stock_level = Column(Integer, default=10, nullable=False)
    supplier = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    blinds_products = relationship("BlindsProduct", back_populates="material")
    warehouse_movements = relationship("WarehouseMovement", back_populates="material")
    reservations = relationship("MaterialReservation", back_populates="material")


class BlindsProduct(Base):
    __tablename__ = "blinds_products"

    id = Column(Integer, primary_key=True, index=True)
    blinds_type_id = Column(Integer, ForeignKey("blinds_types.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    control_type = Column(Enum(ControlType), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    blinds_type = relationship("BlindsType_", back_populates="blinds_products")
    material = relationship("Material", back_populates="blinds_products")
    order_items = relationship("OrderItem", back_populates="product")
    configurations = relationship("ProductConfiguration", back_populates="product")


class ProductConfiguration(Base):
    __tablename__ = "product_configurations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("blinds_products.id"), nullable=False)
    config_name = Column(String(255), nullable=False)
    config_value = Column(String(500), nullable=False)
    price_modifier = Column(Numeric(10, 2), default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    product = relationship("BlindsProduct", back_populates="configurations")


# ==================== Orders ====================
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW, nullable=False, index=True)
    total_price = Column(Numeric(12, 2), nullable=False)
    discount_percentage = Column(Float, default=0, nullable=False)
    final_price = Column(Numeric(12, 2), nullable=False)
    notes = Column(Text, nullable=True)
    measurement_notes = Column(Text, nullable=True)
    delivery_address = Column(Text, nullable=True)
    required_delivery_date = Column(Date, nullable=True)
    actual_delivery_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="orders")
    manager = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")
    production_tasks = relationship("ProductionTask", back_populates="order")
    schedule_items = relationship("ScheduleItem", back_populates="order")
    reservations = relationship("MaterialReservation", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("blinds_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    width_mm = Column(Integer, nullable=False)
    height_mm = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    custom_options = Column(Text, nullable=True)  # JSON-serialized options
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("BlindsProduct", back_populates="order_items")


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    old_status = Column(Enum(OrderStatus), nullable=True)
    new_status = Column(Enum(OrderStatus), nullable=False)
    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="status_history")


# ==================== Warehouse ====================
class WarehouseMovement(Base):
    __tablename__ = "warehouse_movements"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    movement_type = Column(String(50), nullable=False)  # "in", "out", "adjustment"
    quantity = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    reference_id = Column(Integer, nullable=True)  # Order ID or other reference
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    material = relationship("Material", back_populates="warehouse_movements")


class MaterialReservation(Base):
    __tablename__ = "material_reservations"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reserved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    used_at = Column(DateTime, nullable=True)
    is_used = Column(Boolean, default=False, nullable=False)

    # Relationships
    material = relationship("Material", back_populates="reservations")
    order = relationship("Order", back_populates="reservations")


# ==================== Production ====================
class ProductionTask(Base):
    __tablename__ = "production_tasks"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    task_number = Column(String(50), unique=True, nullable=False, index=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="pending", nullable=False)  # pending, in_progress, completed
    priority = Column(Integer, default=0, nullable=False)  # 0=normal, 1=high, 2=critical
    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="production_tasks")
    assigned_to = relationship("User", back_populates="production_tasks")


# ==================== Schedule ====================
class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    installer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_type = Column(String(50), nullable=False)  # "measurement", "installation"
    scheduled_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(10), nullable=True)  # HH:MM format
    end_time = Column(String(10), nullable=True)
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, completed, cancelled
    location = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="schedule_items")
    installer = relationship("User", back_populates="schedule_items")
