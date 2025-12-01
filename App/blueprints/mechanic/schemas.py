from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic
from app.extensions import db
from marshmallow import Schema, fields

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = False
        include_relationships = True
        sqla_session = db.session

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# -------- LOGIN SCHEMA BELOW --------
class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)