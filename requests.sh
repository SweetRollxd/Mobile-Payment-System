#!/bin/bash

echo $(curl -s -X POST localhost:5000/products -H "Content-Type: application/json" -d '{"price": 100500, "description": "lol", "params": {"kek":"lol", "mda":"heh"}}')

echo $(curl -X PATCH localhost:5000/products/1 -H "Content-Type: application/json" -d '{"price": 5, "description": "mda"}')

echo $(curl -X DELETE localhost:5000/products/1)