from fastapi import FastAPI, Request
from .routes import users, supplies, auth
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LabFull API", version="0.0.1")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
@limiter.limit("1/minute")
async def root(request: Request):
    """Returns "Hello, World!"""
    return {"Root": "API documentation is located at http://www.localhost:8000/docs"}
