'''
Query Parameters
'''




# libraries --------
from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional

# App -------
app = FastAPI()

class Book:
    def __init__(self, id: int,
                 title: str,
                 author: str,
                 description: str,
                 published_date: int ,
                 rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date = published_date
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    published_date: int
    rating: int = Field(gt=0, lt=6)

Books = [
    Book(1, 'Coding with Daniel', 'Daniel Jimenez', 'Practices', 2024,5),
    Book(2, 'Coding with Alicia', 'Alicia Jimenez', 'Practices with Ali', 2025, 5),
    Book(3, 'FastApi Masterclass with Emi Jimenez', 'Emilia D. Jimenez', 'Practices with Emi', 2026 ,5)]




# Get Method -------

@app.get('/book')
async def read_all_books():
    return Books

# Acá es donde se valida los paths
@app.get('/book/{book_id}')
async def read_all_books(book_id:int=Path(gt=0)):
    for i in Books:
        if i.id == book_id:
            return i


@app.get('/book/publish_book')
async def publish_book(published_date:int):
    books_to_return = []
    for i in Books:
        if i.published_date == published_date:
            books_to_return.append(i)
    return books_to_return


@app.get('/books/')
async def read_by_rating(book_rating:int = Query(gt=0,lt=6)):
    books_return = []
    for i in Books:
        if i.rating == book_rating:
            books_return.append(i)
        return  books_return

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

async def delete_book(book_id:int=Path(gt=0)):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break