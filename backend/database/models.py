from datetime import datetime
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime

from backend.database.datatypes import LinkPrecedenceTypes
from .connector import Base, db_engine


class User(Base):
    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    phoneNumber = Column(String)
    email = Column(String)
    linkedId = Column(Integer, ForeignKey(id))
    linkPrecedence = Column(Enum(*LinkPrecedenceTypes.all(), name="link_precedence_types"), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime)

# Create all the tables in database
if __name__ == "__main__":
    Base.metadata.create_all(db_engine)