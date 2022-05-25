from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, supplies, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LabFull API", version="0.0.1")


app.include_router(users.router)
app.include_router(supplies.router)
app.include_router(auth.router)


# ROOT
@app.get("/")
async def root():
    """Returns "Hello, World!"""
    return {"Root": "Hello, World!"}
