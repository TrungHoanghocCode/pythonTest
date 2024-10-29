from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException

from pydantic import BaseModel, Field

from starlette import status

app = FastAPI()


# tao 1 object book
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    # nhu la 1 menthod de tham chieu den ngay class nay
    # co tac dung tao 1 book moi, nap vao day
    # published_date
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# List BOOKS sample
BOOKS = [
    Book(1, "DarkSage1212", "Trung", "nice", 5, 1997, ),
    Book(2, "Computer Science Pro", "Fast", "good", 5, 1998),
    Book(3, "Be Fast with FastAPI", "API", "well", 4, 2000),
    Book(4, "Master Endpoints", "Python", "bad", 3, 2005),
    Book(5, "HP1", "API", "awesome", 2, 2010),
    Book(6, "DarkSage2", "Trung", "great", 1, 2020),
]


# Object nay voi tham so (BaseModel)-duoc import voi cac key giong BOOKS
# nham muc dich validate
class BookRequest(BaseModel):
    # id: int
    # title: str
    # author: str
    # description: str
    # rating: int

    # thay cac dieu kien co ban = dieu kien thich hop hon = Field
    # voi id la tuy chon vi user khong biet id nen la so may Optional[int]
    id: Optional[int] = None
    # id: Optional[int] = Field(description = "id is not needed", defaut = None)
    #   = Field(title="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    # doi voi int : gt = min, lt = max
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1980, lt=2025)

    # config nay` nham tao 1 sample value cho user nhin thay khi request book
    class Config:
        json_schema_extra = {
            'example': {
                # 'id' : 9, vi id defaut optional int none nen bo id o day
                'title': 'A new book',
                'author': 'codingWithTrung',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2000
            }
        }


# ham co ban
@app.get("/books", status_code=status.HTTP_200_OK)
# status_code=status.HTTP_200_OK thong bao cho user neu get thanh cong
async def read_all_books():
    return BOOKS


# ham get book theo id (path)
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    # = Path(gt = 0) ~ them dkien cho tham so path
    for book in BOOKS:
        if book.id == book_id:
            return book
    #  lenh raise nham muc dich khi user nhap id ko ton tai => 404
    raise HTTPException(status_code=404, detail='Item not found')


# ham get book theo rating (query)
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    # = Query(gt=0, lt=6) ~ them vao 1 dkien cho tham so query
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# ham get book theo published_date (query)
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1980, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


# # ham post (Body) nham tao them book in books
# # tuong tu da lam o book1
# # tuy nhiên them gi cung duoc, khong dam bao tinh xac thuc
# @app.post("/create-book")
# async def create_book(book_request= Body()):
#     BOOKS.append(book_request)

# dung pydantics de tao mo hinh validate
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
# 201 dung cho cac tac vu create thanh cong
# thay Body()-them gi cung dc = BookRequest ~ BaseModel (them voi dieu kien)
async def create_book(book_request: BookRequest):
    # BOOKS.append(book_request)
    # tao bien moi new_book = converting the request to BOOKS object
    # ** . dict() = dinh dang thanh dictionary
    # new_book = Book(**book_request.dict()) ~ .model_dump
    # new_book = Book(**book_request.dict())
    new_book = Book(**book_request.model_dump())
    # BOOKS.append(new_book)
    BOOKS.append(find_book_id(new_book))


# id phai khac biet doi voi tung book
# tao ham python bthuong (ko async)
# tham so la book voi thuoc tinh la class Book
def find_book_id(book: Book):
    if (len(BOOKS) > 0):
        # BOOKS[-1].id = id cua phan tu cuoi cung trong BOOKS
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    # book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# ham update book
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
# 204 dung cho cac tac vu thay doi ma khong tra ve gi ca
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            # neu co su thay doi thi book_changed : true
            book_changed = True
    # neu ko co su thay doi thi 404
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


# ham del book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
