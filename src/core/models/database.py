import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv("./.env")

host = os.getenv("PGHOST")
port = os.getenv("PGPORT")
user = os.getenv("PGUSER")
password = os.getenv("PGPASSWORD")
database = os.getenv("PGDATABASE")
dbtype = "postgresql"

SQLALCHEMY_DATABASE_URL = f"{dbtype}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine( SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()