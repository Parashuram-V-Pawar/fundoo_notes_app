from fastapi import FastAPI
from src.config.db import Base, engine
from src.models import users, notes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return '{message:"Hello world"}'