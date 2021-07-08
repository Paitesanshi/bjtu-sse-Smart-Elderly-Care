from model.old_person_info import OldPersonInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import logging
from model import guardian

Session = sessionmaker(bind=sqlInit.db)


def get_old_person_info_by_id(id):
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.id==id,OldPersonInfo.REMOVE==0).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_old_person_info_by_name(username):
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.username==username,OldPersonInfo.REMOVE==0).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_old_person_info_list(page,pagesize,username):
    session = Session()
    try:
        if username=='':
            result = session.query(OldPersonInfo).limit(
                pagesize).offset((page - 1) * pagesize).all()
        else:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.username.like("%"+username+"%"),OldPersonInfo.REMOVE==0).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result
def get_old_person_info_count(content):
    session = Session()
    try:
        if content=='':
            result = session.query(OldPersonInfo).count()
        else:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.username.like("%"+content+"%")).count()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def add_old_person_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,imgset_dir,profile_photo,room_number,
                              firstguardian_name,firstguardian_relationship, firstguardian_phone, firstguardian_wechat
                              ,secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state):
    session = Session()
    person=OldPersonInfo(username=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                           checkin_date=checkin_date,checkout_date=checkout_date,imgset_dir=imgset_dir,
                           profile_photo=profile_photo,room_number=room_number,
                           firstguardian_name=firstguardian_name,firstguardian_wechat=firstguardian_wechat,firstguardian_phone=firstguardian_phone,
                           firstguardian_relationship=firstguardian_relationship,secondguardian_name=secondguardian_name,secondguardian_relationship=secondguardian_relationship,secondguardian_phone=secondguardian_phone,
                           secondguardian_wechat=secondguardian_wechat,health_state=health_state)
    try:
        result = session.add(person)
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True

def update_oldperson_info_by_id(id,username,password,REAL_NAME,SEX,EMAIL,
                       PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATEBY,UPDATEBY,
                       REMOVE):
    session = Session()

    user=OldPersonInfo(id=id,username=username,password=password,REAL_NAME=REAL_NAME,SEX=SEX,EMAIL=EMAIL,PHONE=PHONE,MOBILE=MOBILE,
                 DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,CREATEBY=CREATEBY,UPDATEBY=UPDATEBY,REMOVE=REMOVE)
    try:
        u = user.__dict__
        u.pop("_sa_instance_state")
        row= session.query(OldPersonInfo).filter(OldPersonInfo.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True

def delete_old_person_info_by_id(id):
    session = Session()
    try:
        session.query(OldPersonInfo).filter(OldPersonInfo.id==id).update({'REMOVE':1})
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True
