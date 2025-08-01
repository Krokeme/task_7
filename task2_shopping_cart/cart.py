import json
import os
from math import ceil

CART_FILE = "cart.json"



def load_cart():
    if os.path.exists(CART_FILE):
        with open(CART_FILE, "r") as f:
            return json.load(f)
    return []



def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=4)



def add_to_cart(cart, product, qty):
    for item in cart:
        if item["product_id"] == product.id:
            item["qty"] += qty
            return cart
    cart.append({
        "product_id": product.id,
        "name": product.name,
        "price": product.price,
        "qty": qty
    })
    return cart



def calculate_total(cart):
    total = sum(item["price"] * item["qty"] for item in cart)
    return round(ceil(total * 100) / 100, 2)
