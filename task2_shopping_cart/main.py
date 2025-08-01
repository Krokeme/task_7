from fastapi import FastAPI
from pydantic import BaseModel
from cart import load_cart, save_cart, add_to_cart, calculate_total

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float



products = [
    Product(id=1, name="Laptop", price=250.75),
    Product(id=2, name="Mouse", price=15.40),
    Product(id=3, name="Keyboard", price=35.60),
]



cart = load_cart()



@app.get("/products/")
def get_products():
    return products



@app.post("/cart/add")
def add_to_cart(product_id: int, qty: int = 1):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        return {"error": "Product not found"}
    if qty <= 0:
        return {"error": "Quantity must be at least 1"}

    updated_cart = add_to_cart(cart, product, qty)
    save_cart(updated_cart)
    return {"message": "Added to cart", "cart": updated_cart}



@app.get("/cart/checkout")
def checkout():
    if not cart:
        return {"message": "Cart is empty"}
    total = calculate_total(cart)
    return {"items": cart, "total": total}
