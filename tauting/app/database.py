import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

def create_tables():
    from app.models import SQLModel  # Import models before creating tables
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session