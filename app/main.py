from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db





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

#get posts
@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}


#route for sqlalchemy
#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return {"data": posts}


#get posts
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #bew_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get one post
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return{"post_detail": post}

#delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #index = find_index_post(id)
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} doesn't exist")  
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit
    return post_query.first()


