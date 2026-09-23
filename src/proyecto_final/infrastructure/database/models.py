from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    customer: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    items: Mapped[list[OrderItemModel]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    product: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    order: Mapped[OrderModel] = relationship(
        back_populates="items",
    )
