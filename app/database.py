#Near every project this is same#

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}/"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Password already changed but kept the old one for reference to remember
#This one is only for documentation purposes. We do not need now because postgres will do everything

"""
while True:    

    try:
        conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='ArzumKuzum2134-', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error", error)
        time.sleep(2)

"""



