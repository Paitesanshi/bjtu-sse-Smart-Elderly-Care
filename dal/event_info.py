from model.event_info import EventInfo
from common import sqlInit
from sqlalchemy.orm import sessionmaker
import logging
Session = sessionmaker(bind=sqlInit.db)
def get_event_info_by_id(id):
    session = Session()
    try:
        result = session.query(EventInfo).filter(EventInfo.id==id).first()
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return None
    session.close()
    return result

def add_event_info(event_type,event_date,event_location,event_desc,oldperson_id):
    session = Session()
    user=EventInfo(event_type=event_type,event_date=event_date,event_location=event_location,event_desc=event_desc,oldperson_id=oldperson_id)
    try:
        result = session.add(user)
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True
def delete_old_person_info_by_id(id):
    session = Session()
    try:
        session.query(EventInfo).filter(EventInfo.id==id).delete()
        session.commit()
    except Exception as e:
        logging.ERROR(e)
        return False
    session.close()
    return True