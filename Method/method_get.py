## GET HTTP Request Method

# Description
# Create method_get.py



## Code ------

from fastapi import FastAPI, Body

app=FastAPI(version='0.01')

## Create a list of books -------

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

### Dynamic Param -------

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

### Generate Query Parameters -------
@app.get("/books/")
async def read_category_by_query(category:str):
    books_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_return.append(book)
    return books_return


@app.get("/books/{book_author}/")
async def read_category_by_query_author(category: str,
                                        book_author: str):
    books_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and \
                book.get('author').casefold() == book_author.casefold():
            books_return.append(book)

    return books_return

### Using Post Request -----
# Used to create data

@app.post("/books/create_book")
async  def create_book(new_book=Body()):
    BOOKS.append(new_book)

## Put Method ----
# Update Date

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


### Delete Method ------
# Delete


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


'''
get all books from a specific author using query parameters
'''

@app.get("/books/byauthor/{author}")
async def read_books_by_author(author:str):
    book_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            book_return.append(book)


