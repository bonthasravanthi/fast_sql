from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas

from database import Base, engine, SessionLocal
from auth import verify_admin, verify_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------- Database Session ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Product APIs ----------------

# Get all products (Logged-in users)
@app.get("/products", response_model=List[schemas.ProductResponse])
def read_all_products(
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    return crud.get_products(db)


# Get product by ID (Logged-in users)
@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    product = crud.get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# Create product (Admin only)
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_admin)
):
    return crud.create_product(db, product)


# Update product (Admin only)
@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_admin)
):
    updated_product = crud.update_product(
        db,
        product_id,
        product
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product


# Delete product (Admin only)
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_admin)
):
    deleted_product = crud.delete_product(
        db,
        product_id
    )

    if not deleted_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }


# Get products by category (Logged-in users)
@app.get("/category/{category}")
def get_products_category(
    category: str,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    return crud.get_products_by_category(
        db,
        category
    )


# ---------------- User APIs ----------------

# Register User
@app.post("/register_user")
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(user, db)


# Login User
@app.post("/login")
def login_user(
    response: Response,
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.login_user(
        user,
        db,
        response
    )