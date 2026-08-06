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


# ---------------- Home ----------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Product Management API",
        "status": "Running",
        "documentation": "/docs"
    }


# ---------------- Database Session ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Product APIs ----------------

# Create Product (Admin only)
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    return crud.create_product(db, product)


# Read All Products (User & Admin)
@app.get("/products", response_model=List[schemas.ProductResponse])
def read_all_products(
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    return crud.get_products(db)


# Read Product by ID (User & Admin)
@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    product = crud.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# Update Product (Admin only)
@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    updated = crud.update_product(db, product_id, product)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated


# Delete Product (Admin only)
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    deleted = crud.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


# Get Products by Category
@app.get("/products/category/{category}", response_model=List[schemas.ProductResponse])
def get_products_by_category(
    category: str,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    return crud.get_products_by_category(db, category)


# ---------------- Authentication ----------------

# Register
@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(user, db)


# Login
@app.post("/login")
def login(
    user: schemas.UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    return crud.login_user(user, db, response)


# Logout
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}