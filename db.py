from models import *
from pymongo import MongoClient
from fastapi import HTTPException
import os

# Leer el host desde variables de entorno (docker-compose lo proporciona)
mongo_host = os.getenv("MONGO_HOST", "localhost")

# Configuramos la base de datos 
client = MongoClient(host=mongo_host, port=27017)
db = client["Products-mercado-libre"]
coleccion = db["products"]

def insert_product(products: Product_data) -> str:
    """ Inserta nuevos datos a la base de datos """
    try:
        product = [p.dict(exclude_none=True) for p in products.products] 
        coleccion.insert_many(product)
        return {"Message": "Productos guardados con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {e}")

def serialize_doc(doc):
    """ Convierte el ObjectId a string """
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def list_all_products():
    try:
        products = coleccion.find()
        list_products = [serialize_doc(p) for p in products]
        return list_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar datos: {e}")

