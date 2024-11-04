from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg
from psycopg.rows import dict_row 
import multipart


app = FastAPI()

# base model for validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg.connect(
        host='localhost',
        dbname='fastapi',  # Use dbname instead of database
        user='postgres',
        password='amarjinish',
        row_factory=dict_row   # This will return each row as a dictionary
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Database connection failed")
    print("Error:", error)
    time.sleep(2)

    

# hard coded data
cursor.execute("""SELECT * FROM posts""")
all_posts = cursor.fetchall()

def find_post(id):
    for p in all_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i , p in enumerate(all_posts):
        if p['id'] == id:
            return i

#get fields

@app.get("/")
def root():
    return {"message": "Welcome to my api bro !"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# getting values from body using this post method

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data": new_post}
    
@app.get('/posts/latest')
def get_latest_post():
    post = all_posts[len(all_posts)-1]
    return {"details": post}

# title string, content string, category, bool published 
@app.get('/posts/{id}')  # id field here is a path parameter
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))  # Pass id as a tuple
    posts = cursor.fetchone()
    if posts is None:
        response.status_code = 404
        return {"error": "Post not found"}
    return {"data": posts}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))  # Pass id as a tuple
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id: {id}, was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'post with id: {id} was not found'}
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"message": f'updated the post '}