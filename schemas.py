from pydantic import BaseModel


# ---------------------- Product Schemas ----------------------

class ProductCreate(BaseModel):
    name: str
    category: str
    brand: str
    price: int
    color: str


class ProductResponse(ProductCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------------------- User Schemas ----------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    is_admin: bool

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: str
    password: str