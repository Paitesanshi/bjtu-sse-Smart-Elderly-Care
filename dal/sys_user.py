from model.sys_user import SysUser
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import or_
from model import guardian

Session = sessionmaker(bind=sqlInit.db)


def get_sys_user_by_id(id):
    session = Session()
    try:
        result = session.query(SysUser).filter(SysUser.id==id).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result
def get_sys_user_by_username(username):
    session = Session()
    try:
        result = session.query(SysUser).filter(SysUser.username==username).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_sys_user_count(name):
    session = Session()
    try:
        result = session.query(SysUser).filter(or_(SysUser.username.like("%"+name+"%"),
                                                   SysUser.REAL_NAME.like("%"+name+"%"))).count()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_sys_user_info_list(page,pagesize,name):
    session = Session()
    try:
        result = session.query(SysUser).filter(or_(SysUser.username.like("%"+name+"%"),
                                                   SysUser.REAL_NAME.like("%"+name+"%"))).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def add_sys_user(username,password,REAL_NAME,SEX,EMAIL,
                       PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATEBY,
                       REMOVE):
    session = Session()
    user=SysUser(username=username,password=password,REAL_NAME=REAL_NAME,SEX=SEX,EMAIL=EMAIL,PHONE=PHONE,MOBILE=MOBILE,
                 DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,CREATEBY=CREATEBY,REMOVE=REMOVE)
    try:
        result = session.add(user)
        session.commit()
        print(result)
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True
def update_sys_user_by_id(id,username,password,REAL_NAME,SEX,EMAIL,
                       PHONE,MOBILE,DESCRIPTION,ISACTIVE,UPDATEBY,
                       REMOVE):
    session = Session()

    user=SysUser(id=id,username=username,password=password,REAL_NAME=REAL_NAME,SEX=SEX,EMAIL=EMAIL,PHONE=PHONE,MOBILE=MOBILE,
                 DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,UPDATEBY=UPDATEBY,REMOVE=REMOVE)
    try:
        u=user.__dict__
        u.pop("_sa_instance_state")
        row= session.query(SysUser).filter(SysUser.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True
def delete_old_person_info_by_id(id):
    session = Session()
    try:
        session.query(SysUser).filter(SysUser.id==id).delete()
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True