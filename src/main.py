from fastapi import FastAPI
from .database.database import engine
from .database import models
from .routes import users, supplies, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LabFull API", version="0.0.1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credential=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(supplies.router)
app.include_router(auth.router)


# ROOT
@app.get("/")
async def root():
    """Returns "Hello, World!"""
    return {"Root": "API documentation is located at http://www.localhost:8000/docs"}
