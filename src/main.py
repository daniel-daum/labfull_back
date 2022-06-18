from fastapi import FastAPI
from .routes import users, supplies, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LabFull API", version="0.0.1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
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
