import requests
import random
import json
import string

# host = "http://127.0.0.1"
# port = 5000
host = "http://217.71.129.139"
port = 4428
socket = f"{host}:{port}"

names = ("Арина","София","Арсений","Алексей","Евгений","Денис","Василиса","Александра","Дмитрий","Ева")
surnames = ("Андреева","Блинова","Болдырев","Виноградов","Данилов","Карпов","Косарева","Рябова","Соколов","Соловьева")

product_names = ("Молоко", "Хлеб", "Яйца", "Пирог", "Туалетная бумага", "Суп", "Кошачий корм", "Помидор", "Сок", "Зубная паста")
param_names = ("weight", "color", "length", "width", "material", "expiration date", "manufacturer", "articul", "amount", "production date")

"""
"curl -s -X POST localhost:5000/products -H \"Content-Type: application/json\" -d '{\"price\": 100500, \"description\": \"lol\", \"params\": {\"kek\":\"lol\", \"mda\":\"heh\"}}'"
"curl -s -X PATCH localhost:5000/products/1 -H "Content-Type: application/json" -d '{"price": 5, "description": "mda"}'"
"curl -s -X DELETE localhost:5000/products/1"
"curl -s -X POST localhost:5000/users -H "Content-Type: application/json" -d '{"phone": 9138185430, "password": "secret_password", "firstname": "Anton", "lastname": "Antonov"}'"
"curl -s -X PATCH localhost:5000/users/1 -H "Content-Type: application/json" -d '{"firstname": "Petr", "lastname": "Ivanov"}'"
"curl -s -X DELETE localhost:5000/users/1"
"""

tests = [
    ("POST", "/products/", ""),
    # ("GET")
    ("POST", "/users/", "")

]

headers = {
    "Content-Type": "application/json"
}


def random_phone():
    digits = string.digits
    return "".join(random.choice(digits) for i in range(10))


def random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def print_response(response):
    if response.status_code not in (200, 201):
        print(f"Status code {response.status_code}. Response: {response.text}")
    else:
        print(json.loads(response.text))


def create_product(price, desc, params):
    data = {
        "price": price,
        "description": desc,
        "params": params
    }
    response = requests.post(f"{socket}/products", json.dumps(data), headers=headers)
    product_id = response.json()["product_id"]
    return product_id


def create_user(phone, password, firstname, surname):
    data = {
        "phone": phone,
        "password": password,
        "firstname": firstname,
        "surname": surname
    }
    response = requests.post(f"{socket}/users", json.dumps(data), headers=headers)
    user_id = response.json()["user_id"]
    return user_id


def add_to_cart(user_id, product_id, quantity):
    data = {
        "product_id": product_id,
        "quantity": quantity
    }
    response = requests.post(f"{socket}/users/{user_id}/cart", json.dumps(data), headers=headers)
    return json.loads(response.text)


# new_product_params = {}
# for i in range(0,3):
#     new_product_params[random.choice(param_names)] = int(random.random() * 100)
# product_id = create_product(round(random.random() * 1000, 2), random.choice(product_names), new_product_params)
# print(f"Added product ID: {product_id}")


# user_id = create_user(random_phone(), random_string(8), random.choice(names), random.choice(surnames))
# print(f"Added user ID: {user_id}")

#
# products = requests.get(f"{socket}/products").json()
# product_ids = []
# for product in products:
#     product_ids.append(product["product_id"])
# product_id = random.choice(product_ids)
# res = add_to_cart(user_id=5, product_id=product_id, quantity=random.randrange(1, 100))
# print(f"Added to Cart: {res}")
#
#
# products = requests.get(f"{socket}/users/{user_id}/cart").json()
# product_ids = []
# for product in products:
#     product_ids.append(product["product_id"])
# response = requests.delete(f"{socket}/users/{user_id}/cart/{random.choice(product_ids)}")
# print(f"Deleted product from Cart: {response.text}")

# response = requests.delete(f"{socket}/users/{4}/cart")
# print(f"Cart cleared. Deleted products: {json.loads(response.text)}")

response = requests.post(f"{socket}/users/{5}/purchases")
print_response(response)

# money = round(random.random() * 100000, 2)
# print(money)
# response = requests.post(f"{socket}/users/{5}/deposit", json={"amount": money})
# print_response(response)

# kek
# for test in tests:
#     method, endpoint, data = test
#     url = f"{host}:{port}{endpoint}"
#     print(f"{method} {url} with data {data}")
#     # requests.request(f"{host}:{port}/")