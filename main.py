from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "¡Hi my good Friend FastApi!"

@app.get("/url")
async def url():
    return {"url":"https://agura.dev" }


    