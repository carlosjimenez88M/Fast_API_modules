'''
CRUD Method
'''

# Description --------------
# Create -> Post
# Read ->   Get
# Update -> Put
# Delete -> Delete


#=====================#
# Code -------------  #
#=====================#

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

# App ---------
app = FastAPI()

class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

Books = [
    Book(1, 'Coding with Daniel', 'Daniel Jimenez', 'Practices', 5),
    Book(2, 'Coding with Alicia', 'Alicia Jimenez', 'Practices with Ali', 5)
]

# Get Method -------

@app.get('/book')
async def read_all_books():
    return Books

# Post Method -------

@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    new_book = find_book_id(new_book)
    Books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

def find_book_id(book: Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1
    else:
        book.id = 1
    return book

# Update Method -----------

@app.put('/books/update_book')
async def update_book(book_request: BookRequest):
    for i in range(len(Books)):
        if Books[i].id == book_request.id:
            Books[i] = Book(**book_request.dict())
            return {"message": "Book updated successfully", "book": Books[i]}
    return {"message": "Book not found"}




## Delete method --------

@app.delete('/books/delete_books')

async def delete_book(book_id:int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break