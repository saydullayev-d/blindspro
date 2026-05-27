from sqlalchemy.orm import Session
from app.db.models import User, UserRole
from app.db.schemas import UserCreate, UserUpdate, UserResponse
from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password
from app.core.exceptions import ConflictError, NotFoundError
from typing import Optional, List


class UserService:
    """User business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create new user"""
        # Check if email already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ConflictError(f"User with email {user_data.email} already exists")
        
        # Check if username already exists
        existing_user = self.repository.get_by_username(user_data.username)
        if existing_user:
            raise ConflictError(f"Username {user_data.username} already exists")
        
        # Create user
        user_dict = user_data.dict()
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
        return self.repository.create(user_dict)
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.repository.get_by_email(email)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.repository.get_by_username(username)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username/email and password"""
        user = self.repository.get_by_email_or_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user"""
        user = self.get_user(user_id)
        user_dict = user_data.dict(exclude_unset=True)
        return self.repository.update(user_id, user_dict)
    
    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[List[User], int]:
        """List users with pagination"""
        users = self.repository.get_all(skip, limit)
        total = self.repository.get_total_count()
        return users, total
    
    def search_users(self, query: str, skip: int = 0, limit: int = 100) -> tuple[List[User], int]:
        """Search users"""
        users = self.repository.search(query, skip, limit)
        total = len(users)
        return users, total
    
    def get_users_by_role(self, role: UserRole) -> List[User]:
        """Get users by role"""
        return self.repository.get_by_role(role)
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate user"""
        return self.repository.update(user_id, {"is_active": False})
    
    def activate_user(self, user_id: int) -> User:
        """Activate user"""
        return self.repository.update(user_id, {"is_active": True})
