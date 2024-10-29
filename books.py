# import fastapi
from fastapi import Body, FastAPI

# ham co ban dau tien, trang web chay thi keu den app
app = FastAPI()

# khai bao list BOOKS basic
BOOKS = [
    {'title': 'Title 1', 'author': 'Author I', 'category': 'science'},
    {'title': 'Title 2', 'author': 'Author II', 'category': 'science'},
    {'title': 'Title 3', 'author': 'Author III', 'category': 'history'},
    {'title': 'Title 4', 'author': 'Author IV', 'category': 'math'},
    {'title': 'Title 5', 'author': 'Author V', 'category': 'math'},
    {'title': 'Title 6', 'author': 'Author II', 'category': 'math'},
    # {'title': 'Title 1', 'author': 'Author II', 'category': 'science'}
]

# voi trang host co duoi /books thi thuc hien ham nay
# link mau: http://127.0.0.1:8000/books
@app.get("/books")
async def read_all_books():
    return BOOKS


# ham doc title (path)
# /{} se tao nen 1 tham so dynamic => {}=tham so cho ham async
# link mau: http://127.0.0.1:8000/books/Title%20One
@app.get("/books/{book_title}")
async def read_book_title_path(book_title: str):
    # loop qua BOOKS
    for book in BOOKS:
        # ham get lay duoc key title
        # so cai get duoc voi tham so book_title => if true return book
        if book.get('title').casefold() == book_title.casefold():
            return book


# ham doc category (query)
# thay vi add tham so vao link dan
# /books/ : them 1 / cho phep tao 1 query: add category va nhan ket qua
# link mau: http://127.0.0.1:8000/books/?category=math
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        # tuong tu get title nhung ko return ma` chen` book vao list return
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# ket hop ca 2 path va query (Author 2 + math ?)
@app.get("/books/{book_author}/")
# nap tham so va duong dan
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        # if dung author va category thi chen vao [], sau do return []
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# import them BODY
# ph.thuc post => Body() => new_book
# luc go~ tren UI thi chu y dung ""
@app.post("/books/create_book")
# voi new_book = 1 {} new duoc them vao
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# update voi BOOKS[i].title = update
@app.put("/books/update_book")
# voi updated_book = 1 {} co title == va category or author or .... !=
async def update_book(updated_book=Body()):
    # loop BOOKS
    for i in range(len(BOOKS)):
        # if title == thi update
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            break


# delete voi book_title
@app.delete("/books/delete_book/{book_title}")
# voi tham so o day la str book_title
async def delete_book(book_title: str):
    # loop
    for i in range(len(BOOKS)):
        # if BOOKS[i].title = book_title da duoc nhap => del
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            # phuong thuc xoa
            BOOKS.pop(i)
            break


# bai tap fetch all book from 1 author

# @app.get("/books/authors/")
# async def read_author_by_query(author: str):
#     books_author = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_author.append(book)
#     return books_author


# @app.get("/books/byauthor/")
# async def read_books_by_author_path(author: str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_to_return.append(book)
#
#     return books_to_return

#
@app.get("/books/Author/{book_author}")
async def read_book_author_path(book_author: str):
    books_author = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            books_author.append(book)
            return books_author
