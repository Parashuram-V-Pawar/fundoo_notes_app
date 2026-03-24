from fastapi import FastAPI
from src.config.db import Base, engine
from src.models import users
from src.routes import users_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(users_routes.router)