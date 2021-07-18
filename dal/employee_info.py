from model.employee_info import EmployeeInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime


Session = sessionmaker(bind=sqlInit.db)


def get_employee_info_by_id(id):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.id==int(id),EmployeeInfo.REMOVE==0).first()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_info_by_username(username):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.username==username,EmployeeInfo.REMOVE==0).first()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_count(content):
    session = Session()
    try:
        if content==None:
            result = session.query(EmployeeInfo).filter(EmployeeInfo.REMOVE==0).count()
        else:
            result = session.query(EmployeeInfo).filter(EmployeeInfo.username.like("%"+content+"%"),EmployeeInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_info_count_by_id(content):   
    session = Session()
    try:
        if content==None:
            result = session.query(EmployeeInfo).count()
        else:
            result = session.query(EmployeeInfo).filter(EmployeeInfo.ID==content,EmployeeInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result    

def get_employee_hire_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.hire_date>=today,EmployeeInfo.hire_date<=tomorrow,EmployeeInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_count_by_remove(remove):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.REMOVE==remove).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_count_by_gender(sex):
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.gender==sex,EmployeeInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result    


def get_employee_resign_count_by_day(today,tomorrow):   
    session = Session()
    try:
        result = session.query(EmployeeInfo).filter(EmployeeInfo.resign_date>=today,EmployeeInfo.resign_date<=tomorrow,EmployeeInfo.REMOVE==0).count()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def get_employee_info_list(page,pagesize,username):
    session = Session()
    try:
        if username==None:
            result = session.query(EmployeeInfo).filter(EmployeeInfo.REMOVE==0).limit(
                pagesize).offset((page - 1) * pagesize).all()
        else:
            result = session.query(EmployeeInfo).filter(EmployeeInfo.username.like("%" + username + "%"),EmployeeInfo.REMOVE==0).limit(pagesize).offset((page-1)*pagesize).all()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return result

def add_employee_info(username,gender,phone,id_card,birthday,hire_date,DESCRIPTION,ISACTIVE,CREATEBY,REMOVE=0):
    session = Session()
    person=EmployeeInfo(username=username,gender=gender,phone=phone,id_card=id_card,birthday=birthday,
                        hire_date=hire_date,profile_photo=id_card+".jpg",
                        DESCRIPTION=DESCRIPTION,ISACTIVE=ISACTIVE,CREATEBY=CREATEBY,
                        REMOVE=REMOVE)
    p=None                    
    try:
        result = session.add(person)
        session.flush()
        p=sqlInit.query_to_dict(person)
        # session.query(EmployeeInfo).filter(EmployeeInfo.id==p.id).update({'imgset_dir':p.id,'profile_photo':p.id+".jpg"})
        session.commit()
    except Exception as e:
        logging.error(e)
        return None
    session.close()
    return p


def update_employee_info_by_id(id,username,gender,phone,id_card,birthday,hire_date,DESCRIPTION,UPDATEBY):
    session = Session()

    person = EmployeeInfo(id=id, username=username, gender=gender, phone=phone, id_card=id_card, birthday=birthday,
                          hire_date=hire_date, 
                          DESCRIPTION=DESCRIPTION, UPDATEBY=UPDATEBY)
    try:
        u = person.__dict__
        u.pop("_sa_instance_state")
        row= session.query(EmployeeInfo).filter(EmployeeInfo.id==id).update(u)
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True


def delete_employee_info_by_id(id,UPDATEBY):
    session = Session()
    try:
        dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.query(EmployeeInfo).filter(EmployeeInfo.id==id).update({'REMOVE':1,'resign_date':dt,'UPDATEBY':UPDATEBY})
        session.commit()
    except Exception as e:
        logging.error(e)
        return False
    session.close()
    return True