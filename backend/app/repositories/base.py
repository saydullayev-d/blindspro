from typing import Optional, List, Generic, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

T = TypeVar('T')


class BaseRepository(Generic[T]):
    \"\"\"Base repository with common CRUD operations\"\"\"
    
    def __init__(self, db: Session, model: type):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        \"\"\"Get single record by ID\"\"\"
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        \"\"\"Get all records with pagination\"\"\"
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj_in: dict) -> T:
        \"\"\"Create new record\"\"\"
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: int, obj_in: dict) -> Optional[T]:
        \"\"\"Update existing record\"\"\"
        db_obj = self.get_by_id(id)
        if db_obj:
            for key, value in obj_in.items():
                if value is not None:
                    setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        \"\"\"Delete record\"\"\"
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def get_total_count(self) -> int:
        \"\"\"Get total count of records\"\"\"
        return self.db.query(self.model).count()
