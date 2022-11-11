from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'appuser'
    appuser_id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.String, nullable=False)
    passwd = sa.Column(sa.String, nullable=False)
    firstname = sa.Column(sa.String)
    lastname = sa.Column(sa.String)
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated = sa.Column(sa.DateTime)

    __table_args__ = (
        sa.CheckConstraint("length(phone) = 10 and phone ~ '^\d+$'"),
    )

    purchases = relationship("Purchase", back_populates="user")
    shopping_cart = relationship("ShoppingCart", back_populates="user")
    transactions = relationship("FinanceLog", back_populates="user")


class Product(db.Model):
    product_id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric, nullable=False)
    description = sa.Column(sa.String)
    params = sa.Column(sa.JSON)
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated = sa.Column(sa.DateTime)


class State(db.Model):
    state_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)


products_in_purchase = db.Table("purchase_product",
                                sa.Column("purchase_id", sa.Integer, sa.ForeignKey("purchase.purchase_id")),
                                sa.Column("product_id", sa.Integer, sa.ForeignKey("product.product_id")))


class Purchase(db.Model):
    purchase_id = sa.Column(sa.Integer, primary_key=True)
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"))
    # discount = sa.Column(sa.)
    purchase_state = sa.Column(sa.Integer, sa.ForeignKey("state.state_id"))
    purchase_datetime = sa.Column(sa.DateTime, default=datetime.now())
    total = sa.Column(sa.Numeric)

    user = relationship("User", back_populates="purchases")
    products = relationship("Product", secondary=products_in_purchase)
    state = relationship("State")
    transaction = relationship("FinanceLog", back_populates="purchase")


class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"), primary_key=True)
    product_id = sa.Column("product_id", sa.Integer, sa.ForeignKey("product.product_id"), primary_key=True)
    quantity = sa.Column(sa.Integer)

    user = relationship("User", back_populates="shopping_cart")
    products = relationship("Product")


class FinanceLog(db.Model):
    __tablename__ = "finance_log"
    transaction_id = sa.Column(sa.Integer, primary_key=True)
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"))
    transaction_datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    purchase_id = sa.Column(sa.Integer, sa.ForeignKey("purchase.purchase_id"))
    debet = sa.Column(sa.Numeric)
    credit = sa.Column(sa.Numeric)
    saldo = sa.Column(sa.Numeric, nullable=False)

    user = relationship("User", back_populates="transactions")
    purchase = relationship("Purchase", back_populates="transaction")
