from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Inventory
from app.extensions import db

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)