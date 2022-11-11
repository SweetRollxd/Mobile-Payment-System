#!/bin/bash

echo $(curl -s -X POST localhost:5000/products -H "Content-Type: application/json" -d '{"price": 100500, "description": "lol", "params": {"kek":"lol", "mda":"heh"}}')


