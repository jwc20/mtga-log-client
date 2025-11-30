from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import pages, decks, logs


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield
    print("shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_logging_middleware(request: Request, call_next):
    print(f"Request path: {request.url.path}")
    response: Response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response


app.include_router(pages.router)
app.include_router(decks.router)
app.include_router(logs.router)