from pydantic import BaseModel

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