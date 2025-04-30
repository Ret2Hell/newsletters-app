import logging
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import newsletters
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Newsletters API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(newsletters.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app.router.lifespan_context = lifespan
