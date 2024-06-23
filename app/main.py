from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from.routers import post, user





models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Password already changed but kept the old one for reference to remember
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


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "pizza", "id": 2}]


#find a post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
#find index of the post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        


app.include_router(post.router)
app.include_router(user.router)


#get posts
@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}



