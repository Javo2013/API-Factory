from .extensions import db
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

ticket_mechanic = Table(
    "ticket_mechanic",
    db.Model.metadata,
    Column("ticket_id", Integer, ForeignKey("service_tickets.id")),
    Column("mechanic_id", Integer, ForeignKey("mechanics.id")),
)

class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    service_tickets = relationship(
        "ServiceTicket",
        secondary=ticket_mechanic,
        back_populates="mechanics"
    )

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = Column(Integer, primary_key=True)
    issue_description = Column(String(255), nullable=False)
    amount_quoted = Column(Integer)
    amount_charged = Column(Integer)

    mechanics = relationship(
        "Mechanic",
        secondary=ticket_mechanic,
        back_populates="service_tickets"
    )