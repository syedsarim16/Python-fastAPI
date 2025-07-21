#we can copy this code only we need to change the database connection string 
# like the database name, username, password, host and port
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db_connection():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#we dont need this anymore because we are using SQLAlchemy ORM
#while True:
    # Connect to the database
    #try:
       # conn = psycopg2.connect ( host='localhost', database='fastapi',user="postgres",password="sarim@123",
                             #cursor_factory=RealDictCursor) # Replace with your actual password 
        #cursor=conn.cursor()
        #print("Database connection successful")
        #break
    #except Exception as error:
        #print("Database connection failed")
        #print(f"Error: "  ,error)
        #time.sleep(2)
