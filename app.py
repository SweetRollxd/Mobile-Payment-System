from flask import Flask, request
from alembic.config import Config as alembic_Config
from alembic import command as alembic_cmd
from datetime import datetime
import json

from models import db, User, Product, Purchase, ShoppingCart, FinanceLog, State

# db = SQLAlchemy()
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
    if request.method == "POST":
        product_data = request.json
        new_product = Product(price=product_data["price"],
                              description=product_data["description"],
                              params=product_data["params"])

        db.session.add(new_product)
        db.session.commit()
        return {"product_id": new_product.product_id}

    else:
        product_list = Product.query.all()
        print(product_list)
        response = []
        for i, prod in enumerate(product_list):
            print(model_as_dict(prod))
            response.append(model_as_dict(prod))
        return response


@app.route("/products/<int:product_id>", methods=["GET", "PATCH", "DELETE"])
def product(product_id):
    prod = Product.query.get_or_404(product_id)
    if request.method == "GET":
        return model_as_dict(prod)
        # return model_as_dict(Product.query.get(product_id))

    elif request.method == "PATCH":
        changed_data = request.json
        prod.update(changed_data)
        # db.session.query(Product).filter(Product.id == product_id)\
        #     .update(changed_data)
        db.session.commit()
        return Product.query.get_or_404(product_id)
    else:
        db.session.query(Product).filter(Product.id == product_id)\
            .delete()
    return {"msg": "Not ready yet"}, 404


@app.route("/users", methods=["POST"])
def users():
    user = User(phone='9123456789', passwd='lol', firstname='Heh', lastname='Mda')
    db.session.add(user)
    db.session.commit()
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>", methods=["GET", "PATCH", "DELETE"])
def user(user_id):
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>/cart", methods=["GET", "POST", "DELETE"])
def shop_cart(user_id):
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>/cart/<product_id>", methods=["DELETE"])
def delete_product_in_cart(user_id, product_id):
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>/purchases", methods=["POST"])
def pay_pruchase(user_id):
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>/deposit", methods=["POST"])
def deposit(user_id):
    return {"msg": "Not ready yet"}, 404


@app.route("/users/<user_id>/history", methods=["GET"])
def user_history(user_id):
    return {"msg": "Not ready yet"}, 404


if __name__ == '__main__':
    app.run(debug=True)
