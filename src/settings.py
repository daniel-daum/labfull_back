import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv("./.env")

class Settings(BaseSettings):
    DBTYPE:str = os.getenv("DBTYPE")
    DBUSER:str = os.getenv("DBUSER")
    DBPASS:str = os.getenv("DBPASS")
    DBHOST:str = os.getenv("DBHOST")
    DBPORT:str = os.getenv("DBPORT")
    DBNAME:str = os.getenv("DBNAME")
    DBSTR:str = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"

    KEY:str = os.getenv("KEY")
    ALGO:str = os.getenv("ALGO")
    EXPIRE:str = os.getenv("EXPIRE")

settings = Settings()
