#引入要使用的declarative_base
from sqlalchemy.ext.declarative import declarative_base
#在要映射的数据表students中有id，name两个字段，所以要引入Integer对应id，String对应name
from sqlalchemy import Column, Integer, String,DateTime,CHAR
#声名Base
Base = declarative_base()
#User类就是对应于 __tablename__ 指向的表，也就是数据表students的映射
class SysUser(Base):
#students表是我本地数据库testdab中已存在的
    __tablename__ = 'sys_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50),nullable=False)
    SEX=Column(String(5))
    PHONE=Column(String(50))
    theme=Column(String(45))
    DESCRIPTION=Column(String(200))
    ISACTIVE=Column(String(10))
    CREATED=Column(DateTime)
    CREATEDBY=Column(Integer)
    UPDATE=Column(DateTime)
    UPDATEBY=Column(Integer)
    REMOVE=Column(CHAR)

    __table_args__ = {
        "mysql_charset": "utf8"
    }