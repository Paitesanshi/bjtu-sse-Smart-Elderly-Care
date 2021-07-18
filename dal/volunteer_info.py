from model.volunteer_info import VolunteerInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

Session = sessionmaker(bind=sqlInit.db)


def get_volunteer_info_by_id(id):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.id==id,VolunteerInfo.REMOVE==0).first()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_volunteer_info_by_name(name):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.name==name,VolunteerInfo.REMOVE==0).first()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_volunterr_info_count(username):
    session = Session()
    try:
        if username==None:
            result = session.query(VolunteerInfo).filter(VolunteerInfo.REMOVE==0).count()
        else:
            result = session.query(VolunteerInfo).filter(VolunteerInfo.name.like("%" + username + "%"),VolunteerInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_volunterr_info_list(page,pagesize,username):
    session = Session()
    try:
        if username==None:
            result = session.query(VolunteerInfo).filter(VolunteerInfo.REMOVE==0).limit(
            pagesize).offset((page - 1) * pagesize).all()
        else:
            result = session.query(VolunteerInfo).filter(VolunteerInfo.name.like("%" + username + "%"),VolunteerInfo.REMOVE==0).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_volunteer_checkin_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.checkin_date>=today,VolunteerInfo.checkin_date<=tomorrow,VolunteerInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result   
def get_volunteer_count_by_remove(remove):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.REMOVE==remove).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_volunteer_count_by_gender(sex):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.gender==sex,VolunteerInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result       

def get_volunteer_checkout_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.checkout_date>=today,VolunteerInfo.checkout_date<=tomorrow,VolunteerInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result  

def add_volunteer_info(username,gender,phone,id_card,birthday,checkin_date,
                            DESCRIPTION,CREATEBY):
    session = Session()
    person=VolunteerInfo(name=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                        checkin_date=checkin_date,profile_photo=id_card+".jpg",DESCRIPTION=DESCRIPTION,CREATEBY=CREATEBY,REMOVE=0)
    p=None
    try:
        result = session.add(person)
        session.flush()
        p=sqlInit.query_to_dict(person)
        # session.query(VolunteerInfo).filter(VolunteerInfo.id==p.id).update({'imgset_dir':p.id,'profile_photo':p.id+".jpg"})
        session.commit()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return p

def update_volunteer_info_by_id(id,username,gender,phone,id_card,birthday,checkin_date,checkout_date,DESCRIPTION,UPDATEBY):
    session = Session()

    person = VolunteerInfo(id=id,name=username, gender=gender, phone=phone, id_card=id_card, birthday=birthday,
                           checkin_date=checkin_date,checkout_date=checkout_date,DESCRIPTION=DESCRIPTION, UPDATEBY=UPDATEBY)
    try:
        u = person.__dict__
        u.pop("_sa_instance_state")
        row= session.query(VolunteerInfo).filter(VolunteerInfo.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True

def delete_volunteer_info_by_id(id,UPDATEBY):
    session = Session()
    try:
        dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.query(VolunteerInfo).filter(VolunteerInfo.id==id).update({'REMOVE':1,'checkout_date':dt,'UPDATEBY':UPDATEBY})
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True