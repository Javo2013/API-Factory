from app.extensions import db
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


# ----------------------------------------------------
# JUNCTION TABLE: SERVICE TICKET <-> MECHANIC
# ----------------------------------------------------
ticket_mechanic = Table(
    "ticket_mechanic",
    db.Model.metadata,
    Column("ticket_id", Integer, ForeignKey("service_tickets.id")),
    Column("mechanic_id", Integer, ForeignKey("mechanics.id")),
)


# ----------------------------------------------------
# JUNCTION TABLE: SERVICE TICKET <-> PARTS (Inventory)
# ----------------------------------------------------
ticket_parts = Table(
    "ticket_parts",
    db.Model.metadata,
    Column("ticket_id", Integer, ForeignKey("service_tickets.id")),
    Column("part_id", Integer, ForeignKey("inventory.id")),
)


# ----------------------------------------------------
# MECHANIC MODEL
# ----------------------------------------------------
class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)

    service_tickets = relationship(
        "ServiceTicket",
        secondary=ticket_mechanic,
        back_populates="mechanics"
    )


# ----------------------------------------------------
# SERVICE TICKET MODEL
# ----------------------------------------------------
class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = Column(Integer, primary_key=True)
    issue_description = Column(String(255), nullable=False)
    amount_quoted = Column(Integer)
    amount_charged = Column(Integer)

    # Many-to-many with mechanics
    mechanics = relationship(
        "Mechanic",
        secondary=ticket_mechanic,
        back_populates="service_tickets"
    )

    # Many-to-many with parts
    parts = relationship(
        "Inventory",
        secondary=ticket_parts,
        back_populates="tickets"
    )


# ----------------------------------------------------
# INVENTORY MODEL (Part Description)
# ----------------------------------------------------
class Inventory(db.Model):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)

    tickets = relationship(
        "ServiceTicket",
        secondary=ticket_parts,
        back_populates="parts"
    )