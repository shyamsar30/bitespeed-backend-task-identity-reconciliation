from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from backend.database.models import User

class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        load_instance = True