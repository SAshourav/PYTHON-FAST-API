from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg
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
        row_factory=dict  # This will return each row as a dictionary
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Database connection failed")
    print("Error:", error)
    time.sleep(2)

    

# hard coded data
my_post = [{'title': 'title of post 1', 'content': 'content of post 1', 'id':1},
           {'title': 'Favorite Food', 'content': 'I like pizza', 'id':2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i , p in enumerate(my_post):
        if p['id'] == id:
            return i

#get fields

@app.get("/")
def root():
    return {"message": "Welcome to my api bro !"}

@app.get("/posts")
def get_posts():
    return {"data": my_post}

# getting values from body using this post method

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    print(post.dict())
    # return {"new_post": f'{new_post.title} and {new_post.content} is it published? {new_post.published}. Rating: {new_post.rating}'}
    post_dict = post.dict()
    post_dict['id']= randint(0,100000)
    my_post.append(post_dict)
    return {"data": post_dict}
    
@app.get('/posts/latest')
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {"details": post}

# title string, content string, category, bool published 
@app.get('/posts/{id}') #id field here is a path parameter
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id: {id}, was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'post with id: {id} was not found'}
    return {"post details": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    
    my_post.pop(index)
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