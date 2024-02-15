
# Install FastAPI: pip3 install "fastapi[all]"
from fastapi import FastAPI
# Import products as file
from routers import products, users
from fastapi.staticfiles import StaticFiles

#http://127.0.0.1:8000/

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hi, Welcome to this Mockup API, it's a project to learn FastAPI, Enjoy!"

@app.get("/url")
async def url():
    return {"url":"https://agura.dev" }


    