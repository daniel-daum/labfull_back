from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LabFull API", version="0.0.1")

tags_metadata = [{
    "name":"users",
    "description":"Operations with users."
}]

app.include_router(users.router)


# ROOT
@app.get("/")
async def root():
    """Returns "Hello, World!"""
    return {"Root":"Hello, World!"}