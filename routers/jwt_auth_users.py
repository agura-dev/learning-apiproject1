from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#Algorithm to use on encryption
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = "3a219f3ef563968fca836428d4a56abd6cc5219c602390664c5903efe5a5717b"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

#Encryption context
#Define an algorithm for encryption
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel): #BaseModel help us to create an entity
    username: str
    full_name: str
    email: str
    disable: bool

#Entity for user in DB
class UserDB(User):
    password: str

#Capi2023*
#Pao1988*

users_db = {
    "aguradev":{
        "username": "aguradev",
        "full_name": "Adrian Gura",
        "email": "agura.tech@gmail.com",
        "disable": False,
        "password": "$2a$12$FTx1xh7uQ422bitWevyereP5GMnxZp4Q4vswgZIz4h1CMPC24pswO"
    },
    "cirodev":{
        "username": "cirodev",
        "full_name": "Ciro Gutierrez",
        "email": "adgr.dev@gmail.com",
        "disable": True,
        "password": "$2a$12$E/eLusKWtup1GFWRXcQyoe2qSK6jUN9HwvcFXeRQL5JpoSrl0uYuq"
    },
}

#Function to search user in DB
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #**
    
#Function to search the username in the entity user
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid credentials",
        headers={"www-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

#Creamos un criterio de dependencia entre funciones para devolver el usuario sin información sensible
async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Deactivated User")
    
    return user

#Authentication function
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password invalid")

    access_token = {"sub":user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)): #Criterios de Dependencia
    return user