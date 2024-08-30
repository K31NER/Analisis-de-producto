import streamlit as st 
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from io import BytesIO
import time
    
#configuaramos la pagina 
st.set_page_config(
    page_title="Scraperml",
    page_icon="https://cdn-icons-png.flaticon.com/512/1508/1508873.png",
)
#ponemos un titulo a la pagina
st.title("Analisis de producto -:orange[Mercado libre]")

#recibimos el producto a buscar
producto = st.text_input("Que producto desea analizar", placeholder="nombre del producto")

#creamos las listas para almacenas los producto en un diccionario 
lista_nombres = []
lista_precios = []
lista_puntuacion = []
puntuacion_float = []
lista_links = []
#lista_de_ventas = []

#funcion para mostrar el precio de mejor manera
def formatear_precio(precio_num):
    return f"{precio_num:,.0f}" 

#definimos los paises 
paises = ['Colombia','México']

#definimos un diccionario con su pais y url
urls_mercado_libre = {
    'Colombia': 'https://listado.mercadolibre.com.co/',
    'México': 'https://listado.mercadolibre.com.mx/'
}

#creamos el cuadro de eleccion
pais_elegido = st.selectbox("Selecciona un pais: ", paises)

#modificamos el url
if pais_elegido in urls_mercado_libre:
    website = f"{urls_mercado_libre[pais_elegido]}{producto}"
    respuesta = requests.get(website)#hacemos la solicitud 
    contenido = respuesta.content#extraemos el contenido 
    #verificamos la conexion
    soup = BeautifulSoup(contenido,'html.parser')#extraemos el contenido
    #buscamos todas las etiquetas (div) con la clase que contiene toda la informacion del producto 
    productos = soup.find_all('div', class_ = 'ui-search-result__wrapper')
    #obtenemos el link del producto 
    enlaces_productos = soup.find_all('a',class_='poly-component__title')


for producto in productos:
    nombre_productos = producto.find('h2', class_ = 'poly-box').text
    precio_productos = producto.find('span', class_='andes-money-amount__fraction').text
    puntuacion_producto = producto.find('span', class_='poly-reviews__rating')
    link = producto.find("a")["href"]#extraemos los links
    
    #volvemos a hacer web scraping ( este proceso relentiza notablemente el programa)
    #descripcion_producto = requests.get(link)
    #contenido_link = descripcion_producto.content
    #soup2 = BeautifulSoup(contenido_link,'html.parser')
    #venta_elemento = soup2.find_all('span',class_='ui-pdp-subtitle')
    #obtenemos solo el texto
    #venta_texto = venta_elemento[0].text.strip()
    #lista_de_ventas.append(venta_texto)
    
    #verificamos si el producto tiene calificacion y lo limpiamos (usando reasignacion de variable)
    if puntuacion_producto:
        puntuacion_limpia = puntuacion_producto.string # la volvemos string para limpiar las etiquetas HTML
        puntuacion_producto = puntuacion_limpia# reasignamos valor
        puntuacion = float(puntuacion_producto) #volvemos float pararealizar calculos 
        p_float_a_str = str(puntuacion)#volvemios str para eliminar ceros
        puntuacion_sin_ceros = p_float_a_str.replace("0", "")#quitamos los ceros 
        puntuacion_producto = puntuacion_sin_ceros#volvemos a reasignar 
        puntuacion_float.append(puntuacion) 
    #si no tiene puntuacion(es decir es None) la definimos en cero
    else:
        puntuacion_producto = 0 
    #llenamos las listas
    #limpiamos el precio para convertirlo
    Precio_limpio =  precio_productos.replace("$", "").replace(".", "").replace(",", "").replace("US","")
    precio_real = int(Precio_limpio)#lo convertimos
    #agregamos informacion a las listas
    lista_nombres.append(nombre_productos)
    lista_precios.append(precio_real)
    lista_puntuacion.append(puntuacion_producto)
    lista_links.append(link)


#creamos un data frame
df =  pd.DataFrame({
        'nombre': lista_nombres,
        'precio': lista_precios,
        'puntuacion' : lista_puntuacion,
        #'Estado - Ventas' : lista_de_ventas,
        'links de compra': lista_links
    })
#ordenamos en base al precio, no necesitamos poner indice ya que pandas lo pone pordefecto 
df_ordenado = df.sort_values(by='precio')

#creamos el objeto BytesIO para escribir el excel
output = BytesIO()
#escribimos el archivo
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False)

#creamos el boton para buscar
buscar = st.button("buscar")

#damos funcion al boton de buscar
if buscar:
    with st.spinner("Realizando búsqueda..."):
        time.sleep(3) 
    try:
        #creamos las variables para realizar las operaciones 
        numero_de_calificaciones = len(puntuacion_float)
        suma_de_calificacion = sum(puntuacion_float)
        calificacion_promedio = round((suma_de_calificacion/numero_de_calificaciones),1)
        mayor_precio = max(lista_precios)
        menor_precio = min(lista_precios)
        total_precio = sum(lista_precios)  
        total_productos = len(lista_precios) 
        precio_promedio = total_precio/total_productos
        
        #hacemos los valores legibles, reasignadoles el mismo valores pero procesado por la funcion
        precio_promedio = formatear_precio(precio_promedio)
        mayor_precio = formatear_precio(mayor_precio)
        menor_precio = formatear_precio(menor_precio)
        #generamos las columnas
        c1,c2,c3,c4 = st.columns(4)
        #mostramos en la pagina en formato de metrica
        with c1:    
            st.metric(label="Calificacion promedio:" ,value= calificacion_promedio)
        with c2:
            st.metric(label="Precio promedio:", value=precio_promedio)
        with c3:
            st.metric(label="Mayor precio:",value=mayor_precio)
        with c4:
            st.metric(label="Menor precio:", value=menor_precio)
            
        st.dataframe(df)#al usar este metodo nos permite descargarlo como csv
        st.write("Grafica de relacion puntuacion-precio")

        #creamos las columnas para las graficas
        g1,g2 = st.columns(2)
        #mostramos la grafica de comparacion puntuacion precio
        with g1:
            st.line_chart(df_ordenado,x='precio', y='puntuacion')
        with g2:
            st.scatter_chart(df_ordenado[['puntuacion','precio']],x='precio', y='puntuacion', width=600, height=350,)
        
        #creamos el boton de descarga
        descargar_excel = st.download_button(
            label="Descargar datos como Excel",#nombre
            data=output,#tipo de dato
                file_name="lista de productos.xlsx",#nombre del archivo
                mime="application/vnd.ms-excel"
        )              
    except ZeroDivisionError:#al sacarpromedio prevenimos el error de division entre cero
        st.warning("Verifique los parametros y vuelva a buscar por favor")
