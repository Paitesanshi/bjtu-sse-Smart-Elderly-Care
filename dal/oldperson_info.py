from model.old_person_info import OldPersonInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import logging
from datetime import datetime
Session = sessionmaker(bind=sqlInit.db)


def get_old_person_info_by_id(id):    ##改
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.ID==id,OldPersonInfo.REMOVE==0).all()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_old_person_info_by_name(username):
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.username==username,OldPersonInfo.REMOVE==0).first()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_old_person_info_list(page,pagesize,username):
    session = Session()
    try:
        if username==None:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.REMOVE==0).limit(
                pagesize).offset((page - 1) * pagesize).all()
        else:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.username.like("%"+username+"%"),OldPersonInfo.REMOVE==0).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result
def get_old_person_info_count(content):
    session = Session()
    try:
        if content==None:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.REMOVE==0).count()
        else:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.username.like("%"+content+"%"),OldPersonInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_old_person_info_count_by_remove(remove):
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.REMOVE==remove).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_old_person_info_count_by_id(content):   
    session = Session()
    try:
        if content==None:
            result = session.query(OldPersonInfo).count()
        else:
            result = session.query(OldPersonInfo).filter(OldPersonInfo.ID==content,OldPersonInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result
def get_old_person_checkin_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.checkin_date>=today,OldPersonInfo.checkin_date<=tomorrow,OldPersonInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_old_person_count_by_gender(sex):
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.gender==sex,OldPersonInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result    

def get_old_person_checkout_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(OldPersonInfo).filter(OldPersonInfo.checkout_date>=today,OldPersonInfo.checkout_date<=tomorrow,OldPersonInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result    

def add_old_person_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,imgset_dir,profile_photo,room_number,
                              firstguardian_name,firstguardian_relationship, firstguardian_phone, firstguardian_wechat
                              ,secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state,DESCRIPTION,CREATEBY):
    session = Session()
    person=OldPersonInfo(username=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                           checkin_date=checkin_date,checkout_date=checkout_date,imgset_dir=imgset_dir,
                           profile_photo=profile_photo,room_number=room_number,
                           firstguardian_name=firstguardian_name,firstguardian_wechat=firstguardian_wechat,firstguardian_phone=firstguardian_phone,
                           firstguardian_relationship=firstguardian_relationship,secondguardian_name=secondguardian_name,secondguardian_relationship=secondguardian_relationship,secondguardian_phone=secondguardian_phone,
                           secondguardian_wechat=secondguardian_wechat,health_state=health_state,DESCRIPTION=DESCRIPTION,CREATEBY=CREATEBY,REMOVE=0)
    p={}
    try:
        result = session.add(person)
        session.flush()
        p=sqlInit.query_to_dict(person)
        # session.query(OldPersonInfo).filter(OldPersonInfo.id==p.id).update({'imgset_dir':p.id,'profile_photo':p.id+".jpg"})
        session.commit()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return p

def update_oldperson_info_by_id(ID,username,gender,phone,id_card,birthday,checkin_date,checkout_date,imgset_dir,profile_photo,room_number,
                              firstguardian_name,firstguardian_relationship, firstguardian_phone, firstguardian_wechat
                              ,secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state,DESCRIPTION,UPDATEBY):
    session = Session()

    person=OldPersonInfo(ID=ID,username=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                           checkin_date=checkin_date,checkout_date=checkout_date,imgset_dir=imgset_dir,
                           profile_photo=profile_photo,room_number=room_number,
                           firstguardian_name=firstguardian_name,firstguardian_wechat=firstguardian_wechat,firstguardian_phone=firstguardian_phone,
                           firstguardian_relationship=firstguardian_relationship,secondguardian_name=secondguardian_name,secondguardian_relationship=secondguardian_relationship,secondguardian_phone=secondguardian_phone,
                           secondguardian_wechat=secondguardian_wechat,health_state=health_state,DESCRIPTION=DESCRIPTION,UPDATEBY=UPDATEBY)
    try:
        u = person.__dict__
        u.pop("_sa_instance_state")
        row= session.query(OldPersonInfo).filter(OldPersonInfo.ID==ID).update(u)
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True

def delete_old_person_info_by_id(id,UPDATEBY):
    session = Session()
    try:
        dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.query(OldPersonInfo).filter(OldPersonInfo.ID==id).update({'REMOVE':1,'checkout_date':dt,'UPDATEBY':UPDATEBY})
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True
