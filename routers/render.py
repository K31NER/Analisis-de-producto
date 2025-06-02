from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Renderizar html"])

template = Jinja2Templates(directory="templates")

@router.get("/")
async def inicio(request:Request):
    return template.TemplateResponse("index.html",{"request":request})