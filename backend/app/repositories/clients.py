from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.db.models import Client, ClientNote, InteractionStatus
from app.repositories.base import BaseRepository
from typing import Optional, List


class ClientRepository(BaseRepository[Client]):
    """Client data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, Client)
    
    def get_by_email(self, email: str) -> Optional[Client]:
        """Get client by email"""
        return self.db.query(Client).filter(Client.email == email).first()
    
    def get_by_phone(self, phone: str) -> Optional[Client]:
        """Get client by phone"""
        return self.db.query(Client).filter(Client.phone == phone).first()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Search clients by name, email, phone, city"""
        search_term = f"%{query}%"
        return self.db.query(Client).filter(
            or_(
                Client.name.ilike(search_term),
                Client.email.ilike(search_term),
                Client.phone.ilike(search_term),
                Client.city.ilike(search_term),
                Client.company_name.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: InteractionStatus, skip: int = 0, limit: int = 100) -> List[Client]:
        """Get clients by interaction status"""
        return self.db.query(Client).filter(
            Client.interaction_status == status
        ).order_by(desc(Client.created_at)).offset(skip).limit(limit).all()
    
    def get_by_manager(self, manager_id: int, skip: int = 0, limit: int = 100) -> List[Client]:
        """Get clients assigned to manager"""
        return self.db.query(Client).filter(
            Client.manager_id == manager_id
        ).order_by(desc(Client.created_at)).offset(skip).limit(limit).all()
    
    def get_recent(self, limit: int = 20) -> List[Client]:
        """Get recently created clients"""
        return self.db.query(Client).order_by(desc(Client.created_at)).limit(limit).all()


class ClientNoteRepository(BaseRepository[ClientNote]):
    """Client note data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(db, ClientNote)
    
    def get_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[ClientNote]:
        """Get all notes for client"""
        return self.db.query(ClientNote).filter(
            ClientNote.client_id == client_id
        ).order_by(desc(ClientNote.created_at)).offset(skip).limit(limit).all()
    
    def get_latest_by_client(self, client_id: int, limit: int = 10) -> List[ClientNote]:
        """Get latest notes for client"""
        return self.db.query(ClientNote).filter(
            ClientNote.client_id == client_id
        ).order_by(desc(ClientNote.created_at)).limit(limit).all()
