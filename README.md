# 🛒 MercadoLibre Web Scraper

Un proyecto de práctica para web scraping de MercadoLibre utilizando Playwright, con FastAPI como backend y una interfaz web simple.

## 📋 Descripción

Este es un proyecto de aprendizaje enfocado en practicar técnicas de web scraping extrayendo información de productos de MercadoLibre. El objetivo principal es dominar el uso de Playwright para automatización web y crear una base de datos para futuros análisis de datos.

## 🎯 Objetivos del Proyecto

- **Práctica de Web Scraping**: Aprender y perfeccionar técnicas de extracción de datos web
- **Automatización con Playwright**: Dominar el uso de esta herramienta para navegación automatizada
- **Desarrollo de API**: Crear endpoints funcionales con FastAPI
- **Preparación para Análisis**: Recopilar datos estructurados para análisis futuros
- **Interfaz Simple**: Desarrollar una interfaz web básica para interactuar con el scraper

## ✨ Características Actuales

- 🕷️ **Web Scraping**: Extracción automatizada de datos de productos de MercadoLibre
- 🚀 **API REST**: Endpoints básicos desarrollados con FastAPI
- 🌐 **Interfaz Web**: Panel HTML simple para controlar el scraping

## 🔮 Funcionalidades Planificadas

- 📊 **Análisis de Datos**: Procesamiento y análisis de la información recopilada
- 📈 **Visualizaciones**: Gráficos y reportes de tendencias de precios
- 🔍 **Insights de Mercado**: Análisis comparativo de productos y vendedores

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **FastAPI** - Framework web para la API
- **Playwright** - Herramienta de web scraping y automatización
- **HTML/CSS/JavaScript** - Interfaz web básica
- **MongoDB** - Almacenamiento para analisis

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/mercadolibre-scraper.git
   cd mercadolibre-scraper
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar navegadores de Playwright**
   ```bash
   playwright install
   ```

## 🚀 Uso

### Ejecutar la aplicación

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🎓 Aprendizajes

Este proyecto me está ayudando a desarrollar habilidades en:

- **Web Scraping Ético**: Técnicas responsables de extracción de datos
- **Desarrollo de APIs**: Crear endpoints RESTful con FastAPI
- **Automatización Web**: Control programático de navegadores
- **Estructura de Proyectos**: Organización de código Python

## 🔄 Próximos Pasos

### Análisis de Datos (Próximamente)
- Implementar análisis estadístico de precios
- Desarrollar comparativas entre categorías de productos
- Generar reportes automáticos de insights

### Mejoras Técnicas
- Optimizar la velocidad de scraping
- Implementar manejo de errores más robusto
- Mejorar la interfaz de usuario
