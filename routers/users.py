from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users")

'''
router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404:{"message":"not found"}})
'''

## Start the server with: python3 -m uvicorn users:app --reload

'''
@router.get("/")
async def root():
    return "Main page"
'''

#User entity
class User(BaseModel): #BaseModel help us to create an entity
    id: int
    name: str
    lastname: str
    age: int

## Simulamos una DB con una lista
users_list = [User(id = 1, name = "Elena", lastname = "Gutierrez", age = 7),
         User(id = 2, name = "Ciro", lastname = "Herrera", age =  8),
         User(id = 3, name = "Capi", lastname = "Guti", age = 1 ),
         User(id = 4, name = "Orion", lastname = "Palace", age = 6 ),
         ]

''' 
@app.get("/userslocal")
async def userslocal():
    return [{"name": "Elena", "lastname": "Gutierrez", "age": 7},
            {"name": "Ciro", "lastname": "Herrera", "age": 8}]
'''

#Function to get the user list

@router.get("/")
async def users():
    return users_list

#Function to get user by id
#Esta función trabaja con un parametro en el path, lo que significa que se llama
#desde la propio url (Para otro  caso ver proxima función)

'''
@app.get("/user/{id}")
async def user(id: int): #Creamos una nueva función user y se define el tipo de dato que le enviamos
    #HOF Filter
    users = filter (lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}
'''
@router.get("/{id}") #Igualamos una clave con un valor en la URL
async def user(id: int):
    return search_user(id)
    
#Funcion para obtener usuarios por ID
#en esta ocasión usando la query
    
@router.get("/") #Igualamos una clave con un valor en la URL
async def user(id: int): #Agrego parametro de busqueda
    return search_user(id)
    
'''
Podria agregar dos parametros de busqueda co
async def user(id: int, name: str):

en la busqueda, la url seria: ?id=1&name=ciro
'''

#Funcion para crear usuarios usando un post
@router.post("/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="The user already exists")
        #return {"Error": "User already exists in DB"}
    users_list.append(user)
    return user

#Function to update users        
@router.put("/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "User not updated"}
    else:
        return user

#Function to delete users
    
@router.delete("/{id}")
#Le pasamos el id para eliminar
async def user(id: int):
     
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return{"error":"User not deleted"}
        



#Generalizo con una funcion search_user
def search_user(id: int):
    users = filter (lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}
    