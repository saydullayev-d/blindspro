from sqlalchemy.orm import Session
from app.db.models import Client, ClientNote, InteractionStatus
from app.db.schemas import ClientCreate, ClientUpdate, ClientNoteCreate
from app.repositories.clients import ClientRepository, ClientNoteRepository
from app.core.exceptions import NotFoundError
from typing import List, Tuple


class ClientService:
    """Client business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.client_repo = ClientRepository(db)
        self.note_repo = ClientNoteRepository(db)
    
    def create_client(self, client_data: ClientCreate) -> Client:
        """Create new client"""
        client_dict = client_data.dict()
        return self.client_repo.create(client_dict)
    
    def get_client(self, client_id: int) -> Client:
        """Get client by ID"""
        client = self.client_repo.get_by_id(client_id)
        if not client:
            raise NotFoundError("Client", client_id)
        return client
    
    def update_client(self, client_id: int, client_data: ClientUpdate) -> Client:
        """Update client"""
        self.get_client(client_id)
        client_dict = client_data.dict(exclude_unset=True)
        return self.client_repo.update(client_id, client_dict)
    
    def delete_client(self, client_id: int) -> bool:
        """Delete client"""
        self.get_client(client_id)
        return self.client_repo.delete(client_id)
    
    def list_clients(self, skip: int = 0, limit: int = 100) -> Tuple[List[Client], int]:
        """List clients with pagination"""
        clients = self.client_repo.get_all(skip, limit)
        total = self.client_repo.get_total_count()
        return clients, total
    
    def search_clients(self, query: str, skip: int = 0, limit: int = 100) -> Tuple[List[Client], int]:
        """Search clients"""
        clients = self.client_repo.search(query, skip, limit)
        total = len(clients)
        return clients, total
    
    def get_client_by_status(self, status: InteractionStatus, skip: int = 0, limit: int = 100) -> Tuple[List[Client], int]:
        """Get clients by interaction status"""
        clients = self.client_repo.get_by_status(status, skip, limit)
        return clients, len(clients)
    
    def get_recent_clients(self, limit: int = 20) -> List[Client]:
        """Get recently created clients"""
        return self.client_repo.get_recent(limit)
    
    def add_note(self, client_id: int, created_by_id: int, content: str) -> ClientNote:
        """Add note to client"""
        self.get_client(client_id)
        note_data = {
            "client_id": client_id,
            "created_by_id": created_by_id,
            "content": content
        }
        return self.note_repo.create(note_data)
    
    def get_client_notes(self, client_id: int, skip: int = 0, limit: int = 100) -> List[ClientNote]:
        """Get notes for client"""
        self.get_client(client_id)
        return self.note_repo.get_by_client(client_id, skip, limit)
    
    def delete_note(self, note_id: int) -> bool:
        """Delete note"""
        return self.note_repo.delete(note_id)
    
    def update_interaction_status(self, client_id: int, status: InteractionStatus) -> Client:
        """Update client interaction status"""
        return self.update_client(client_id, ClientUpdate(interaction_status=status))
