'''
Status Code
'''



# Descriptions ------------


#1xx -> Information Response: Request Processing
#2xx -> SUccess: Request Successfully complete
#3xx -> Redirection : Futher action must be complete
#4xx -> Client Error : An error was caused by the client
#5xx -> Server Errors: An error occurred on the server


# 2xx Successful Status code

#200:Ok -> Standard Response for a Successful Request
#201:Created -> The request has ben successful , creating a new Resourc, Used when a POST creates an entity
#204: No Content -> Request has been succesful , did not create an entity

# 4xx Client Errors Status Codes :
#400:Bad request -> Cannot Process request due to client error
#401: Unauthorized -> Client dont have authentication for this target resource
#404: Not Found -> Client requested resource can not be found
#422: Unprocessable entity -> Semantic Errors in CLient request

# 5xx Server Status code
#500: Internal Server Error -> Generic error message, when an unexpected issue on the server happened




# libraries --------
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

# App -------
app = FastAPI()

class Book:
    def __init__(self, id: int,
                 title: str,
                 author: str,
                 description: str,
                 published_date: int,
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
    Book(1, 'Coding with Daniel', 'Daniel Jimenez', 'Practices', 2024, 5),
    Book(2, 'Coding with Alicia', 'Alicia Jimenez', 'Practices with Ali', 2025, 5),
    Book(3, 'FastApi Masterclass with Emi Jimenez', 'Emilia D. Jimenez', 'Practices with Emi', 2026, 5)
]

# Get Method -------

@app.get('/book', status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books

@app.get('/book/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=422,
                        detail='id not found')

@app.get('/book/publish_book', status_code=status.HTTP_200_OK)
async def publish_book(published_date: int):
    books_to_return = []
    for book in Books:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_return = []
    for book in Books:
        if book.rating == book_rating:
            books_return.append(book)
    return books_return

# Post Method -------

@app.post('/create-book', status_code=status.HTTP_201_CREATED)
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
            return {"message": "Book updated successfully",
                    "book": Books[i]}
    return {"message": "Book not found"}

# Delete Method --------

@app.delete('/books/delete_books')
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_changed = True
            return {"message": "Book deleted successfully"}
    if not book_changed:
        HTTPException(status_code=422,
                      detail="Book not found")