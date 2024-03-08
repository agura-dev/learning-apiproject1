###  Users DB API  ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

#router = APIRouter(prefix="/usersdb")

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message": "not found"}})

## Start the server with: python3 -m uvicorn users:app --reload

''' 
@app.get("/userslocal")
async def userslocal():
    return [{"name": "Elena", "lastname": "Gutierrez", "age": 7},
            {"name": "Ciro", "lastname": "Herrera", "age": 8}]
'''

#Function to get the user list

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

@router.get("/{id}") #Igualamos una clave con un valor en la URL
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
@router.get("/") #Igualamos una clave con un valor en la URL
async def user(id: str): #Agrego parametro de busqueda
    return search_user("_id", ObjectId(id))
    
'''
Podria agregar dos parametros de busqueda co
async def user(id: int, name: str):

en la busqueda, la url seria: ?id=1&name=ciro
'''

#Funcion para crear usuarios usando un post
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="The user already exists")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))


    return User(**new_user)

#Function to update users        
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "User not updated"}
    
    return search_user("_id", ObjectId(user.id))

#Function to delete users
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
#Le pasamos el id para eliminar
async def user(id: str):
     
    found = db_client.local.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return{"error":"User not deleted"}
        

#Generalizo con una funcion search_user
    #Esta función se generalizo aún más usando los parametros field and key como metodos para buscar
def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error": "User not found"}

    