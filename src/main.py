from fastapi import FastAPI
from .core.models.database import engine
from .core.models import models
from .routes import users, supplies, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LabFull API", version="0.0.1")

app.include_router(users.router)
app.include_router(supplies.router)
app.include_router(auth.router)


# ROOT
@app.get("/")
async def root():
    """Returns "Hello, World!"""
    return {"Root": "API documentation is located at http://www.localhost:8000/docs"}
