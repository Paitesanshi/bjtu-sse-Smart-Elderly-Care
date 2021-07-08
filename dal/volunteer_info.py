from model.volunteer_info import VolunteerInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
from model import guardian

Session = sessionmaker(bind=sqlInit.db)


def get_volunteer_info_by_id(id):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.id==id).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_volunteer_info_by_name(name):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter(VolunteerInfo.name==name).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_volunterr_info_count(criteria):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter_by(criteria).count()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_volunterr_info_list(page,pagesize,criteria):
    session = Session()
    try:
        result = session.query(VolunteerInfo).filter_by(**criteria).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def add_volunteer_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,imgset_dir,
                            profile_photo,DESCRIPTION,ISACTIVE,CREATEDBY,REMOVE):
    session = Session()
    person=VolunteerInfo(name=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                        checkin_date=checkin_date,checkout_date=checkout_date,imgset_dir=imgset_dir,profile_photo=profile_photo,
                        DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,CREATEDBY=CREATEDBY,REMOVE=REMOVE)
    try:
        result = session.add(person)
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True

def update_volunteer_info_by_id(id,username,gender,phone,id_card,birthday,checkin_date,checkout_date,imgset_dir,
                            profile_photo,DESCRIPTION,ISACTIVE,UPDATEBY,REMOVE):
    session = Session()

    person = VolunteerInfo(id=id, name=username, gender=gender, phone=phone, id_card=id_card, birthday=birthday,
                           checkin_date=checkin_date, checkout_date=checkout_date, imgset_dir=imgset_dir,
                           profile_photo=profile_photo,
                           DESCRIPTION=DESCRIPTION, ISACTIVE=ISACTIVE, UPDATEBY=UPDATEBY, REMOVE=REMOVE)
    try:
        u = person.__dict__
        u.pop("_sa_instance_state")
        row= session.query(VolunteerInfo).filter(VolunteerInfo.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True

def delete_volunteer_info_by_id(id):
    session = Session()
    try:
        session.query(VolunteerInfo).filter(VolunteerInfo.id==id).delete()
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True