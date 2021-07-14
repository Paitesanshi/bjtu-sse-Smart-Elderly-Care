#引入要使用的declarative_base
from sqlalchemy.ext.declarative import declarative_base
#在要映射的数据表students中有id，name两个字段，所以要引入Integer对应id，String对应name
from sqlalchemy import Column, Integer, String,DateTime,CHAR
#声名Base
Base = declarative_base()
#User类就是对应于 __tablename__ 指向的表，也就是数据表students的映射
class EmployeeInfo(Base):
#students表是我本地数据库testdab中已存在的
    __tablename__ = 'employee_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50),nullable=False)
    gender=Column(String(5))
    phone=Column(String(50))
    id_card=Column(String(50))
    birthday=Column(DateTime)
    hire_date=Column(DateTime)
    resign_date=Column(DateTime)
    imgset_dir=Column(String(200))
    profile_photo=Column(String(200))
    DESCRIPTION=Column(String(200))
    ISACTIVE=Column(String(10))
    CREATED=Column(DateTime)
    CREATEBY=Column(Integer)
    UPDATED=Column(DateTime)
    UPDATEBY=Column(Integer)
    REMOVE=Column(CHAR)

    __table_args__ = {
        "mysql_charset": "utf8"
    }