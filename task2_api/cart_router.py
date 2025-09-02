from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime
from app.models import Product
from app.database import get_session
from app.auth import get_current_user
from app.utils.order_utils import save_order

router = APIRouter(prefix="/cart", tags=["Cart"])
carts = {}  # in-memory: {username: [{"product_id": 1, "quantity": 2}]}


@router.post("/add/")
def add_to_cart(product_id: int, quantity: int, session: Session = Depends(get_session),
                user: dict = Depends(get_current_user)):
    product = session.get(Product, product_id)
    if not product or product.stock < quantity:
        raise HTTPException(status_code=400, detail="Product not available")
    carts.setdefault(user["username"], []).append({"product_id": product_id, "quantity": quantity})
    return {"message": f"Added {quantity} of {product.name} to cart"}


@router.post("/checkout/")
def checkout(session: Session = Depends(get_session), user: dict = Depends(get_current_user)):
    username = user["username"]
    if username not in carts or not carts[username]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []
    for item in carts[username]:
        product = session.get(Product, item["product_id"])
        if not product or product.stock < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Product {item['product_id']} unavailable")
        product.stock -= item["quantity"]
        session.add(product)
        total += product.price * item["quantity"]
        order_items.append({"name": product.name, "quantity": item["quantity"], "price": product.price})

    session.commit()
    order = {"user": username, "items": order_items, "total": total, "time": datetime.utcnow().isoformat()}

    # Save order
    save_order(order)

    carts[username] = []  # clear cart
    return {"message": "Checkout successful", "order": order}
