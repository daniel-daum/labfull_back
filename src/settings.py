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
    DBNAME_TEST:str = os.getenv("DBNAME_TEST")
    DBSTR:str = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"
    DBSTR_TEST:str = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME_TEST}"

    KEY:str = os.getenv("KEY")
    ALGO:str = os.getenv("ALGO")
    EXPIRE:str = os.getenv("EXPIRE")
    ADMIN:str = os.getenv("ADMIN")
    ROLE:str = os.getenv("ROLE")

settings = Settings()
