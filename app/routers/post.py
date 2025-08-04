from .. import models, schemas
from ..database import get_db_connection
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from fastapi import Response
from .. import oauth2  # Importing the oauth2 module for authentication

router= APIRouter(
    prefix="/posts",
    tags=["Posts"]  # Adding a tag for better organization in the API docs
)


#Working with raw SQL queries or psycopg2
#@router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db_connection),
                 current_user: int = Depends(oauth2.get_current_user),
                 limit: int=10,skip:int=0,search:Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    post= db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(
            limit).offset(
                skip).all() # Using SQLAlchemy ORM to get all posts
     
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(
                models.Post.title.contains(search)).limit(
                    limit).offset(
                        skip).all()

    return (results)

    
   # return (post)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.CreatePost,db: Session = Depends(get_db_connection),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user.email)  # Printing the user_id for debugging purposes
    new_post = models.Post(
        owner_id=current_user.id, **post.dict()
        ) # Creating a new Post object using the Pydantic model data
    db.add(new_post) # Adding the new post to the session
    db.commit()
    db.refresh(new_post) # Refreshing the new post to get the updated data from the database
    return  (new_post)


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db_connection),
                 current_user: int = Depends(oauth2.get_current_user)):
   #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post=cursor.fetchone()
    #print(post)
   # post=db.query(models.Post).filter(models.Post.id == id).first() # Using SQLAlchemy ORM to get a post by id
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first() 

    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
    return (post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db_connection),
                 current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.CreatePost, db: Session = Depends(get_db_connection),
                 current_user: int = Depends(oauth2.get_current_user)):
# cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#(post.title, post.content, post.published, str(id)))
#updated_post=cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id) # Using SQLAlchemy ORM to update a post by id
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit() # Committing the changes to the database
    return post_query.first()

