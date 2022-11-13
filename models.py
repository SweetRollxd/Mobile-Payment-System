from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from datetime import datetime

# from extra_functions import get_datetime

db = SQLAlchemy()


# TODO: добавить констрейнты для created, updated, deleted во всех таблицах


class User(db.Model):
    __tablename__ = 'appuser'
    appuser_id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.String, nullable=False)
    passwd = sa.Column(sa.String, nullable=False)
    balance = sa.Column(sa.Numeric(18, 2), nullable=False, default=0)
    firstname = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.now())
    deleted = sa.Column(sa.Boolean, nullable=False, default=False)
    deleted_at = sa.Column(sa.DateTime)

    __table_args__ = (
        sa.CheckConstraint("length(phone) = 10 and phone ~ '^\d+$'"),
    )

    purchases = relationship("Purchase", back_populates="user")
    shopping_cart = relationship("ShoppingCart", back_populates="user")
    transactions = relationship("FinanceLog", back_populates="user")

    def clear_cart(self):
        removed_product_ids = []
        for cart_row in self.shopping_cart:
            removed_product_ids.append({
                "product_id": cart_row.product_id,
                "quantity": cart_row.quantity
            })
        deleted = db.session.query(ShoppingCart).filter(ShoppingCart.appuser_id == self.appuser_id) \
            .delete()
        return removed_product_ids


class Product(db.Model):
    product_id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric, nullable=False)
    description = sa.Column(sa.String)
    params = sa.Column(sa.JSON)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.now())
    deleted = sa.Column(sa.Boolean, nullable=False, default=False)
    deleted_at = sa.Column(sa.DateTime)

    # purchases = relationship("Purchase", back_populates="product")


class State(db.Model):
    state_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)


# products_in_purchase = db.Table("purchase_product",
#                                 sa.Column("purchase_id", sa.Integer, sa.ForeignKey("purchase.purchase_id")),
#                                 sa.Column("product_id", sa.Integer, sa.ForeignKey("product.product_id")),
#                                 sa.Column("quantity", sa.Integer, nullable=False))

class ProductsInPurchase(db.Model):
    __tablename__ = 'purchase_product'
    purchase_id = sa.Column(sa.Integer, sa.ForeignKey("purchase.purchase_id"), primary_key=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey("product.product_id"), primary_key=True)
    quantity = sa.Column(sa.Integer, nullable=False)

    # purchase = relationship("Purchase", back_populates="products")
    product = relationship("Product")


class Purchase(db.Model):
    purchase_id = sa.Column(sa.Integer, primary_key=True)
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"))
    # discount = sa.Column(sa.)
    purchase_state = sa.Column(sa.Integer, sa.ForeignKey("state.state_id"))
    purchase_datetime = sa.Column(sa.DateTime, default=datetime.now())
    total = sa.Column(sa.Numeric)

    user = relationship("User", back_populates="purchases")
    products = relationship("ProductsInPurchase")
    state = relationship("State")
    transaction = relationship("FinanceLog", back_populates="purchase")


class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"), primary_key=True)
    product_id = sa.Column("product_id", sa.Integer, sa.ForeignKey("product.product_id"), primary_key=True)
    quantity = sa.Column(sa.Integer)

    user = relationship("User", back_populates="shopping_cart")
    products = relationship("Product")

    # TODO: добавить CHECK на положительное quantity


class FinanceLog(db.Model):
    __tablename__ = "finance_log"
    transaction_id = sa.Column(sa.Integer, primary_key=True)
    appuser_id = sa.Column(sa.Integer, sa.ForeignKey("appuser.appuser_id"))
    transaction_datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    purchase_id = sa.Column(sa.Integer, sa.ForeignKey("purchase.purchase_id"))
    debet = sa.Column(sa.Numeric(18, 2))
    credit = sa.Column(sa.Numeric(18, 2))
    saldo = sa.Column(sa.Numeric(18, 2), nullable=False)

    user = relationship("User", back_populates="transactions")
    purchase = relationship("Purchase", back_populates="transaction")
