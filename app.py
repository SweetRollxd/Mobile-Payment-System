from flask import Flask, request
from alembic.config import Config as alembic_Config
from alembic import command as alembic_cmd
from datetime import datetime
from decimal import Decimal
import hashlib
import json

from models import db, User, Product, Purchase, ProductsInPurchase, ShoppingCart, FinanceLog, State

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://sukharik:mypass@localhost/appdb'
alembic_cfg = alembic_Config("alembic.ini")

db.init_app(app)

# with app.app_context():
# db.create_all()

alembic_cmd.upgrade(alembic_cfg, "head")


def get_datetime(date_time):
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


def model_as_dict(model_object):
    dictionary = {}
    for attr in model_object.__table__.columns:
        value = getattr(model_object, attr.name)
        if type(value) is datetime:
            value = get_datetime(getattr(model_object, attr.name))
        dictionary[attr.name] = value
    return dictionary


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login", methods=["POST"])
def login():
    return {"msg": "Not ready yet"}, 404


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        product_list = Product.query.filter(Product.deleted == False).all()
        response = []
        for i, prod in enumerate(product_list):
            response.append(model_as_dict(prod))
        return response

    else:
        product_data = request.json
        new_product = Product(price=product_data["price"],
                              description=product_data["description"],
                              params=product_data["params"])

        db.session.add(new_product)
        db.session.commit()
        return {"product_id": new_product.product_id}, 201


@app.route("/products/<int:product_id>", methods=["GET", "PATCH", "DELETE"])
def product(product_id):
    prod = Product.query.filter(Product.product_id == product_id, Product.deleted == False).first_or_404()
    if request.method == "GET":
        return model_as_dict(prod)

    elif request.method == "PATCH":
        changed_data = request.json
        db.session.query(Product).filter(Product.product_id == product_id) \
            .update(changed_data)
        db.session.commit()
        return {"product_id": product_id}

    else:
        db.session.query(Product).filter(Product.product_id == product_id) \
            .update({"deleted": True, "deleted_at": get_datetime(datetime.now())})
        db.session.commit()
        return {"product_id": product_id}


@app.route("/users", methods=["POST"])
def users():
    user_data = request.json
    new_user = User(phone=user_data["phone"],
                    passwd=hashlib.sha256(user_data["password"].encode()).hexdigest(),
                    firstname=user_data["firstname"],
                    surname=user_data["surname"])
    db.session.add(new_user)
    db.session.commit()
    return {"user_id": new_user.appuser_id}, 201


@app.route("/users/<int:user_id>", methods=["GET", "PATCH", "DELETE"])
def user(user_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    if request.method == "GET":
        usr = model_as_dict(usr)
        usr.pop("passwd")
        return usr

    elif request.method == "PATCH":
        changed_data = request.json
        if "password" in changed_data:
            changed_data["passwd"] = hashlib.sha256(changed_data["password"].encode()).hexdigest()
            changed_data.pop("password")
        db.session.query(User).filter(User.appuser_id == user_id) \
            .update(changed_data)
        db.session.commit()
        return {"user_id": user_id}

    else:
        db.session.query(User).filter(User.appuser_id == user_id) \
            .update({"deleted": True, "deleted_at": get_datetime(datetime.now())})
        db.session.commit()
        return {"user_id": user_id}


@app.route("/users/<int:user_id>/cart", methods=["GET", "POST", "DELETE"])
def shop_cart(user_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    if request.method == "GET":
        cart_list = []
        products_in_cart = db.session.query(Product, ShoppingCart.quantity).join(ShoppingCart.products).filter(ShoppingCart.appuser_id == user_id).all()
        if not products_in_cart:
            return [], 204
        for i, prod in enumerate(products_in_cart):
            prod_data = model_as_dict(prod[0])
            prod_data["quantity"] = prod[1]
            cart_list.append(prod_data)

        return cart_list

    elif request.method == "POST":
        product_id = request.json["product_id"]
        quantity = request.json["quantity"]
        # TODO: ?????????????????? 404 ???????????? ???? 400
        prod = Product.query.filter(Product.product_id == product_id, Product.deleted == False).first_or_404()

        # ???????? ?? ?????????????? ???????????????????????? ?????? ???????? ?????????? ??????????, ???? ???????????????? ???????????????????? ?? ?????? ????????????????????
        if ShoppingCart.query.filter(ShoppingCart.product_id == product_id, ShoppingCart.appuser_id == user_id).first() is not None:
            db.session.query(ShoppingCart).filter(ShoppingCart.appuser_id == user_id, ShoppingCart.product_id == product_id) \
                .update({"quantity": ShoppingCart.quantity + quantity})
        # ?????????? ?????????????????? ?????????? ?? ??????????????
        else:
            new_item = ShoppingCart(appuser_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_item)

        db.session.commit()
        return model_as_dict(prod)

    else:
        product_ids = usr.clear_cart()
        db.session.commit()
        return {"product_ids": product_ids}


@app.route("/users/<int:user_id>/cart/<int:product_id>", methods=["DELETE"])
def delete_product_in_cart(user_id, product_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    prod = ShoppingCart.query.filter(ShoppingCart.appuser_id == user_id, ShoppingCart.product_id == product_id).first_or_404()
    db.session.query(ShoppingCart).filter(ShoppingCart.appuser_id == user_id, ShoppingCart.product_id == product_id) \
        .delete()
    db.session.commit()
    return model_as_dict(prod)


@app.route("/users/<int:user_id>/purchases", methods=["POST"])
def pay_purchase(user_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    products_in_cart = usr.clear_cart()
    if not products_in_cart:
        return [], 204
    # print(products_in_cart)
    new_purchase = Purchase(appuser_id=user_id, purchase_state=1)
    total = 0
    for product in products_in_cart:
        pp_record = ProductsInPurchase(quantity=product["quantity"])
        pp_record.product = Product.query.get(product["product_id"])
        # print(f"Price: {pp_record.product.price}")
        total += pp_record.product.price * pp_record.quantity
        new_purchase.products.append(pp_record)

    print(f"Total: {total}, User balance: {usr.balance}")
    if usr.balance < total:
        return {"msg": "Insufficient Funds"}, 400
    new_purchase.total = total
    transact = FinanceLog(appuser_id=user_id, debet=total, saldo=usr.balance)
    new_purchase.transaction.append(transact)

    User.query.filter(User.appuser_id == user_id).update({"balance": User.balance - total})
    db.session.add(new_purchase)

    db.session.commit()
    return {"purchase_id": new_purchase.purchase_id}, 201


@app.route("/users/<int:user_id>/deposit", methods=["POST"])
def deposit(user_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    credit = Decimal(str(request.json["amount"]))
    transact = FinanceLog(appuser_id=user_id, credit=credit, saldo=usr.balance)
    User.query.filter(User.appuser_id == user_id).update({"balance": User.balance + credit})
    db.session.add(transact)
    db.session.commit()
    return {"balance": usr.balance}


@app.route("/users/<int:user_id>/history", methods=["GET"])
def user_history(user_id):
    usr = User.query.filter(User.appuser_id == user_id, User.deleted == False).first_or_404()
    response = []
    for i, transact in enumerate(usr.transactions):
        response.append(model_as_dict(transact))
    return response


if __name__ == '__main__':
    app.run(debug=True)
