from .database import create_tables
from fastapi import FastAPI
from . import routess  # relative import
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 App is starting up...")
    create_tables()  # Setup DB tables
    print("✅ Tables created.")
    yield
    print("👋 App is shutting down...")

def create_app():
    app = FastAPI(
        description='myfirst app',
        title='idk'
    )
    
    app.include_router(routess.router, prefix="/routes", tags=["Routes"])
    return app
