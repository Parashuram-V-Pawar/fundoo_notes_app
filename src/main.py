from fastapi import FastAPI
from src.config.db import Base, engine
from src.config.logger_middleware import log_requests
from src.models import notes, users
from src.routes import notes_routes  

app = FastAPI()
app.middleware("http")(log_requests)

# Create tables
Base.metadata.create_all(bind=engine)
app.include_router(notes_routes.router)