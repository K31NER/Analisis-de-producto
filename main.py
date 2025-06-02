from models import *
from routers import render
from scraper import scraper_product
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/scraper",response_model=Product_data)
async def scrapear(search:str):
    clean_search = search.strip()
    
    if not clean_search:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
      # Realizamos el scrapeo
    products = await scraper_product(clean_search)
    
    # Devolvemos los valores
    return Product_data(Products=[
        Product(
            nombre=p[0], precio=p[1],puntuacion=p[2],link=p[3],imagen=p[4]
        ) for p in products
    ])
    
app.include_router(render.router)