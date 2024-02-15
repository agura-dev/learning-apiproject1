
#Import APIRouter to route the API to the control file
from fastapi import APIRouter

#Change fastapi to APIRouter

#Generalizamos el prefix para llamar a todas las rutas en la URL
router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses = {404:{"message":"not found"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]