from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
#from fastapi import HTTPException
#Clases que gestionan la autenticación
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

#User entity
class User(BaseModel): #BaseModel help us to create an entity
    username: str
    full_name: str
    email: str
    disable: bool

#Entity for user in DB
class UserDB(User):
    password: str

users_db = {
    "aguradev":{
        "username": "aguradev",
        "full_name": "Adrian Gura",
        "email": "agura.tech@gmail.com",
        "disable": False,
        "password": "Capi2023*"
    },
    "cirodev":{
        "username": "cirodev",
        "full_name": "Ciro Gutierrez",
        "email": "adgr.dev@gmail.com",
        "disable": True,
        "password": "Pao1988*"
    },

}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #**
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
#Creamos un criterio de dependencia entre funciones para devolver el usuario sin información sensible
async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", 
            headers={"www-Authenticate":"Bearer"})
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Deactivated User")
    return user


    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password invalid")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user:User = Depends(current_user)): #Criterios de Dependencia
    return user