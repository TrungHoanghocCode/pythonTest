
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # unique = true => duy nhat
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    # chuc vu : user/ admin, neu la ad thi co 1 so  API dac biet
    hashed_password = Column(String)
    # phan password se duoc ma hoa de khong ai thay duoc
    is_active = Column(Boolean, default=True)
    phone_number = Column(String,)


# khai bao class Todos bang Base vua import
class Todos(Base):
    # là cách để SQLalchemy biết nên đặt tên gì cho bảng này
    # bên trong cơ sở dữ liệu của chúng ta sau này.
    __tablename__ = 'todos'

    # id la 1 khoa chinh - primary_key
    # index : co the hieu la id nay co the tang len
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    # do uu tien
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    # them vao sau khi co User - ForeignKey
    owner_id: Column[int] = Column(Integer, ForeignKey("users.id"))
