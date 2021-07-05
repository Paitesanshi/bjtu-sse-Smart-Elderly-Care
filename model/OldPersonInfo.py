#引入要使用的declarative_base
from sqlalchemy.ext.declarative import declarative_base
#在要映射的数据表students中有id，name两个字段，所以要引入Integer对应id，String对应name
from sqlalchemy import Column, Integer, String,DateTime,Cha
#声名Base
Base = declarative_base()
#User类就是对应于 __tablename__ 指向的表，也就是数据表students的映射
class OldPersonInfo(Base):
#students表是我本地数据库testdab中已存在的
    __tablename__ = 'oldperson_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50),nullable=False)
    gender=Column(String(5))
    phone=Column(String(50))
    id_card=Column(String(50))
    birthday=Column(DateTime)
    checkin_date=Column(DateTime)
    checkout_date=Column(DateTime)
    imgset_dir=Column(String(200))
    profile_photo=Column(String(200))
    room_number=Column(String(50))
    firstguardian_name=Column(String(50))
    firstguardian_relationship=Column(String(50))
    firstguardian_phone=Column(String(50))
    firstguardian_wechat=Column(String(50))
    secondguardian_name=Column(String(50))
    secondguardian_relationship=Column(String(50))
    secondguardian_phone=Column(String(50))
    secondguardian_wechat=Column(String(50))
    health_state=Column(String(50))
    DESCRIPTION=Column(String(200))
    ISACTIVE=Column(String(10))
    CREATED=Column(DateTime)
    CREATEDBY=Column(Integer)
    UPDATE=Column(DateTime)
    UPDATEBY=Column(Integer)
    REMOVE=Column()

    __table_args__ = {
        "mysql_charset": "utf8"
    }