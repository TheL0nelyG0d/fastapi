from automation.automation import current_users
from .. import models, schemas, oauth2
from sqlalchemy import func
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List, Optional


#prefix allows directly add /posts to each post path operation
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



#get posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all
    
    results = db.query(models.Post, func.count(models.Vote.post_id)).label("votes").join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).gorup_by(models.Post.id)
    all()

    return posts

#create posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #bew_post = cursor.fetchone()
    #conn.commit()


    new_post = models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get one post
@router.get("//{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return{"post_detail": post}

#delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()




    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} doesn't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} doesn't exist")  

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit
    return post_query.first()