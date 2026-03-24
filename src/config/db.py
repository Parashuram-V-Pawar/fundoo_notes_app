import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
port = os.getenv('PORT_NUMBER')
database = os.getenv('DATABASE')

DATABASE_URL = (
    f"mssql+pyodbc://{username}:{password}@localhost,{port}/"
    f"{database}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()