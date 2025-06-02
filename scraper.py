import pandas as pd
import asyncio
from playwright.async_api import async_playwright

URL = "https://listado.mercadolibre.com.co/"

# Convertimos la función a async
async def get_image_url(img_tag) -> str:
    """Obtiene el verdadero link de la imagen"""
    if not img_tag:
        return None
    for attr in ["src", "data-src", "data-srcset"]:
        url = await img_tag.get_attribute(attr)
        if url and not url.startswith("data:image"):
            return url
    return None

async def scraper_product(producto: str):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Cargamos la URL
        await page.goto(f"{URL}{producto}", timeout=60000)
        
        # Esperamos que cargen los productos
        await page.wait_for_selector("li.ui-search-layout__item")

        # Obtenemos la lista de productos
        products = await page.query_selector_all("li.ui-search-layout__item")
        lista_productos = []

        for product in products:
            try:
                # Obtemos los datos directo del html
                name = await product.query_selector("h3")
                price = await product.query_selector("span.andes-money-amount__fraction")
                rating = await product.query_selector("span.poly-reviews__rating")
                link = await product.query_selector("a.poly-component__title")
                image = await product.query_selector("img.poly-component__picture")

                if not (name and price and link):
                    continue
                
                # Limpiamos los datos
                clean_name = (await name.inner_text()).strip()
                clean_price = (await price.inner_text()).strip()
                clean_rating = float((await rating.inner_text()).strip()) if rating else 0.0
                clean_link = await link.get_attribute("href")
                clean_image = await get_image_url(image)

                lista_productos.append((clean_name, clean_price, clean_rating, clean_link, clean_image))

            except Exception as e:
                print(f"⚠️ Error procesando un producto: {e}")
                continue

        await browser.close()
        return lista_productos

# Ejecutamos el scraper usando asyncio
if __name__ == "__main__":
    async def main():
        data = await scraper_product("carro")
        df = pd.DataFrame(data, columns=["Nombre", "Precio", "Rating", "Link", "Imagen"])
        print(df.head())
        df.to_csv("productos.csv", encoding="utf-8", index=False)

    asyncio.run(main())
