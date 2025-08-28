from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json
import os
import uuid

from auth import get_current_user, require_role

app = FastAPI(title="Secure Shopping Cart API", version="1.0.0")

PRODUCTS_FILE = "products.json"
CARTS_FILE = "cart.json"




class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

class Product(ProductIn):
    id: str

class CartAddRequest(BaseModel):
    product_id: str
    qty: int = Field(..., gt=0)




def safe_load_json(path: str, default):
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):


        return default

def safe_save_json(path: str, data: Any):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)




@app.post("/admin/add_product/", response_model=Product, status_code=status.HTTP_201_CREATED)
def add_product(payload: ProductIn, user = Depends(require_role("admin"))):
    products: List[Dict[str, Any]] = safe_load_json(PRODUCTS_FILE, default=[])
    new_product = {
        "id": str(uuid.uuid4()),
        "name": payload.name,
        "price": float(payload.price),
    }
    products.append(new_product)
    safe_save_json(PRODUCTS_FILE, products)
    return new_product

@app.get("/products/", response_model=List[Product])
def list_products():
    products: List[Dict[str, Any]] = safe_load_json(PRODUCTS_FILE, default=[])
    return products

@app.post("/cart/add/", status_code=status.HTTP_200_OK)
def add_to_cart(payload: CartAddRequest, user = Depends(get_current_user)):
    # Validate product exists
    products: List[Dict[str, Any]] = safe_load_json(PRODUCTS_FILE, default=[])
    product = next((p for p in products if p["id"] == payload.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    carts: Dict[str, Any] = safe_load_json(CARTS_FILE, default={})

    username = user["username"]
    user_cart: List[Dict[str, Any]] = carts.get(username, [])



    existing = next((item for item in user_cart if item["product_id"] == payload.product_id), None)
    if existing:
        existing["qty"] += int(payload.qty)
    else:
        user_cart.append({"product_id": payload.product_id, "qty": int(payload.qty)})

    carts[username] = user_cart
    safe_save_json(CARTS_FILE, carts)

    return {"message": "Added to cart", "user": username, "item": {"product_id": payload.product_id, "qty": payload.qty}}



@app.get("/health")
def health():
    return {"status": "ok"}
