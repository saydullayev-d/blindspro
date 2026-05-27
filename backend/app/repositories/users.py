from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import User, UserRole
from app.repositories.base import BaseRepository
from typing import Optional, List


class UserRepository(BaseRepository[User]):
    """User data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email_or_username(self, email_or_username: str) -> Optional[User]:
        """Get user by email or username"""
        return self.db.query(User).filter(
            or_(
                User.email == email_or_username,
                User.username == email_or_username
            )
        ).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users"""
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by email, username or full name"""
        search_term = f"%{query}%"
        return self.db.query(User).filter(
            or_(
                User.email.ilike(search_term),
                User.username.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()
