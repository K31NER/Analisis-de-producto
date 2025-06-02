from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    nombre: str
    precio: str
    puntuacion: float
    link: str
    imagen: str
    
class Product_data(BaseModel):
    products: List[Product] = Field(..., alias="Products")

    class Config:
        populate_by_name = True 