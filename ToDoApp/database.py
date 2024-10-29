from sqlalchemy import create_engine
# create_engine là 1 công cụ để kết nối, sử dụng data

from sqlalchemy.orm import sessionmaker
# trình tạo phiên (đéo hiểu)

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
# cong cu khai bao

# URL này tạo vị trí cho database trên app fastapi (chưa hiểu lắm)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db'
# update sau khi connect voi database moi
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:121297@localhost/TodoApplicationDatabase'
# doi voi mySql code se nhu sau:
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:121297@127.0.0.1:3306/TodoApplicationDatabase"

# biến engine này là 1 công cụ link với todoapp.db
# mặc định, SQLite chỉ cho một luồng giao tiếp với nó. - connect_args={'check_same_thread': False}
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
# update
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# (tạo 1 phien cuc bo SessionLocal voi bind=engine ~ SQLALCHEMY_DATABASE_URL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# khai bao nay nhu 1 cach de biet khi nao dung Base se la luc tao 1 base
Base = declarative_base()
