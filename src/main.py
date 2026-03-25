from fastapi import FastAPI
from config.db import Base, engine
from config.logger_middleware import log_requests
from src.models import notes, users
from src.routes import users_routes, notes_routes  

app = FastAPI()
app.middleware("http")(log_requests)

# Create tables
Base.metadata.create_all(bind=engine)
app.include_router(notes_routes.router)
app.include_router(users_routes.router)