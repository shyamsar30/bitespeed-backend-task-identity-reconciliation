from flask import g
from sqlalchemy import or_

from backend.database.models import User
from backend.database.schemas import UsersSchema


db_session = None

def init_db_session(session):
    global db_session
    db_session = session

class GenericDao:
    model = None
    schema = None

    def upsert(self, db_obj):
        g.db_session.add(db_obj)
        g.db_session.commit()
        g.db_session.refresh(db_obj)
        return db_obj
    
class UserDao(GenericDao):
    model = User
    schema = UsersSchema

    def get_complete_record(self, email, phoneNumber):
        return g.db_session.query(
            self.model
        ).filter(
            self.model.email == email,
            self.model.phoneNumber == phoneNumber
        ).all()
    
    def get_partital_record(self, email, phoneNumber):

        if not email:
            email = "dummy"
        if not phoneNumber:
            phoneNumber = "-1"

        return g.db_session.query(
            self.model
        ).filter(
            or_(self.model.email == email, self.model.phoneNumber == phoneNumber)
        ).order_by(self.model.createdAt).all()
    
    def insert_record(self, data):
        db_obj = self.schema().load(data, session=g.db_session)
        return self.upsert(db_obj)
    
    def get_ids_from_email_phone(self, email, phoneNumber):

        if not email:
            email = "dummy"
        if not phoneNumber:
            phoneNumber = "-1"

        return g.db_session.query(
            self.model
        ).filter(
            or_(self.model.email == email, self.model.phoneNumber == phoneNumber)
        ).with_entities(
            self.model.id,
            self.model.linkedId
        ).all()
    
    def get_ids_from_ids(self, ids):
        return g.db_session.query(
            self.model
        ).where(
            or_(self.model.id.in_(ids), self.model.linkedId.in_(ids))
        ).with_entities(
            self.model.id,
            self.model.linkedId
        ).all()
    
    def get_records_by_ids(self, ids):
        return g.db_session.query(
            self.model
        ).where(
            self.model.id.in_(ids)
        ).order_by(
            self.model.createdAt
        ).all()

user_dao_handler = UserDao()