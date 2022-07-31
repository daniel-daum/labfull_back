import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv("./.env")


class Settings(BaseSettings):
    DBTYPE = os.getenv("DBTYPE")
    DBUSER= os.getenv("DBUSER")
    DBPASS= os.getenv("DBPASS")
    DBHOST = os.getenv("DBHOST")
    DBPORT = os.getenv("DBPORT")
    DBNAME= os.getenv("DBNAME")
    DBNAME_TEST = os.getenv("DBNAME_TEST")
    DBSTR = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"
    DBSTR_TEST = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME_TEST}"

    KEY: str = os.getenv("KEY")
    ALGO: str = os.getenv("ALGO")
    EXPIRE: str = os.getenv("EXPIRE")
    ADMIN: str = os.getenv("ADMIN")
    ROLE: str = os.getenv("ROLE")

    EMAIL: str = os.getenv("EMAIL")
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER")
    EMAIL_SERVER_KEY: str = os.getenv("EMAIL_SERVER_KEY")


settings = Settings()
