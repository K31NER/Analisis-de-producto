from db import *
from models import *
from routers import render
from scraper import scraper_product
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/scraper",response_model=Product_data)
async def scrapear(search:str):
    try: 
        clean_search = search.strip()
        
        if not clean_search:
            raise HTTPException(status_code=404, detail="No se encontraron productos")
        # Realizamos el scrapeo
        products_search = await scraper_product(clean_search)
        
        # Devolvemos los valores
        result = [
            Product(
                nombre=p[0],
                precio=p[1],
                puntuacion=p[2],
                link=p[3],
                imagen=p[4]
            ) for p in products_search
        ]
        products = Product_data(Products=result)
        insert_product(products)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {e}")

@app.get("/all_items")
async def retur_all():
    return list_all_products()
app.include_router(render.router)