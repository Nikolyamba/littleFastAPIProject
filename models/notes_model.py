from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database.session import Base

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    context = Column(String(250))
    created_at = Column(DateTime, default=datetime.utcnow())