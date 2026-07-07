from datetime import date
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from .extensions import db

service_mechanics = db.Table(
    "service_mechanics",
    db.Column("service_id", db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)

    service_tickets: Mapped[List['Service']] = db.relationship(back_populates='customer')


class Service(db.Model):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(400), nullable=False)

    customer_id: Mapped[int] = mapped_column(
        db.ForeignKey('customers.id'),
        nullable=False
    )

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')

    mechanics: Mapped[List['Mechanic']] = db.relationship(
        secondary=service_mechanics,
        back_populates="services"
    )


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    services: Mapped[List['Service']] = db.relationship(
        secondary=service_mechanics,
        back_populates="mechanics"
    )