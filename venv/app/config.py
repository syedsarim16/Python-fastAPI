from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__),".env"))
class Settings(BaseSettings):
    database_hostname:str
    database_port:int
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int 
    class Config:
        env_file = ".env"
settings = Settings()

