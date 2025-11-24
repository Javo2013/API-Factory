from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic
from app.extensions import db

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_relationships = True
        sqla_session = db.session

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)