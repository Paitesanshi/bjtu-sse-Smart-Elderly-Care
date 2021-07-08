from model.employee_info import EmployeeInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
from model import guardian

Session = sessionmaker(bind=sqlInit.db)


def get_employee_info_by_id(id):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.id==id).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_employee_info_by_username(username):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.username==username).first()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def get_employee_info_list(page,pagesize,username):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter_by(EmployeeInfo.username.like("%" + username + "%")).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def add_employee_info(username,gender,phone,id_card,birthday,hire_date,resign_date,imgset_dir,
                            profile_photo,DESCRIPTION,ISACTIVE,CREATEDBY,REMOVE):
    session = Session()
    person=EmployeeInfo(username=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                        hire_date=hire_date,resign_date=resign_date,imgset_dir=imgset_dir,profile_photo=profile_photo,
                        DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,CREATEDBY=CREATEDBY,
                        REMOVE=REMOVE)
    try:
        result = session.add(person)
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True

def update_employee_info_by_id(id,username,gender,phone,id_card,birthday,hire_date,resign_date,imgset_dir,
                            profile_photo,DESCRIPTION,ISACTIVE,UPDATEBY,REMOVE):
    session = Session()

    person = EmployeeInfo(id=id, username=username, gender=gender, phone=phone, id_card=id_card, birthday=birthday,
                          hire_date=hire_date, resign_date=resign_date, imgset_dir=imgset_dir,
                          profile_photo=profile_photo,
                          DESCRIPTION=DESCRIPTION, ISACTIVE=ISACTIVE, UPDATEBY=UPDATEBY,
                          REMOVE=REMOVE)
    try:
        u = person.__dict__
        u.pop("_sa_instance_state")
        row= session.query(EmployeeInfo).filter(EmployeeInfo.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True


def delete_employee_info_by_id(id):
    session = Session()
    try:
        session.query(EmployeeInfo).filter(EmployeeInfo.id==id).delete()
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True