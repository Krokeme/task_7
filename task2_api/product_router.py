from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Product
from app.database import get_session
from app.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/admin/", response_model=Product)
def add_product(product: Product, session: Session = Depends(get_session), user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admins only")
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=List[Product])
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()
