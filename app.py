from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import json

from models import db, User
# db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://sukharik:mypass@localhost/appdb'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/register")
def register():
    user = User(phone='9123456789', passwd='lol', firstname='Heh', lastname='Mda')
    db.session.add(user)
    db.session.commit()
    return "Added!"


if __name__ == '__main__':
    app.run(debug=True)

