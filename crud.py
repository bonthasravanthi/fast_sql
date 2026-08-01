from sqlalchemy.orm import Session
import models
import schemas
import bcrypt
from fastapi import Response
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


# ----------------------------- PRODUCT CRUD -----------------------------

def create_product(db: Session, product: schemas.ProductCreate):
    # creating a product object with user values
    db_product = models.Product(**product.model_dump())

    # adding new product to existing table
    db.add(db_product)

    # committing the changes to the database
    db.commit()

    # refreshing the database to get updated values
    db.refresh(db_product)

    # returning response to the user
    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductCreate
):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    db_product.name = product.name
    db_product.category = product.category
    db_product.brand = product.brand
    db_product.price = product.price
    db_product.color = product.color

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    db.delete(db_product)
    db.commit()

    return db_product


def get_products_by_category(db: Session, category: str):
    print(category)
    return db.query(models.Product).filter(
        models.Product.category == category
    ).all()


# --------------------------- USER REGISTRATION ---------------------------

def create_user(user: schemas.UserCreate, db: Session):
    new_user = models.Users(**user.model_dump())

    hashed = bcrypt.hashpw(
        new_user.password.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode()

    new_user.password = hashed

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ------------------------------ USER LOGIN -------------------------------

def login_user(user: schemas.UserLogin, db: Session, response: Response):

    is_exists = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if not is_exists:
        return {"message": "user not found"}

    valid = bcrypt.checkpw(
        user.password.encode(),
        is_exists.password.encode()
    )

    if not valid:
        return {"message": "invalid password"}

    payload = {
        "name": is_exists.name,
        "email": is_exists.email,
        "is_admin": is_exists.is_admin,
        "is_loggedin": True,
        "exp": datetime.utcnow() + timedelta(seconds=30)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return {
        "message": "login successful",
        "access_token": token
    }