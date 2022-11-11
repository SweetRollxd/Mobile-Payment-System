#!/bin/bash

COMMANDS_LIST=(
    "curl -s -X POST localhost:5000/products -H \"Content-Type: application/json\" -d '{\"price\": 100500, \"description\": \"lol\", \"params\": {\"kek\":\"lol\", \"mda\":\"heh\"}}'"
    "curl -s -X PATCH localhost:5000/products/1 -H "Content-Type: application/json" -d '{"price": 5, "description": "mda"}'"
    "curl -s -X DELETE localhost:5000/products/1"
    "curl -s -X POST localhost:5000/users -H "Content-Type: application/json" -d '{"phone": 9138185430, "password": "secret_password", "firstname": "Anton", "lastname": "Antonov"}'"
    "curl -s -X PATCH localhost:5000/users/1 -H "Content-Type: application/json" -d '{"firstname": "Petr", "lastname": "Ivanov"}'"
    "curl -s -X DELETE localhost:5000/users/1"
)
IFS='
'
for COMMAND in $COMMANDS_LIST
do
    RESULT=$($COMMAND)
    echo $RESULT
done
