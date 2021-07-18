from datetime import datetime
from datetime import timedelta
from flask import Flask, Blueprint, request, make_response, jsonify, render_template
from dal import oldperson_info,sys_user,event_info,employee_info,volunteer_info
from common import sqlInit,redisInit
from common import util
import os
import json
from dateutil.parser import parse, parser
index_page = Blueprint("index_page", __name__)
events=['老人笑','摔倒','陌生人出现','禁区闯入','义工和老人交互']

def make_success_response(data,message):
    response={}
    response['code']='success'
    response['message']=message
    response['data']=data
    return response
def make_error_response(data,messsage):
    response={}
    response['code']='error'
    response['message']=messsage
    response['data']=data
    return response

# @index_page.route("/")
# def text():
#     return "text/html"


@index_page.route("/text_same")
def text_same():
    response = make_response("text/html", 200)
    return response


@index_page.route("/json")
def json():
    import json
    data = {"a": "b"}
    response = make_response(json.dumps(data))
    response.headers["Content-Type"] = "application/json"
    return response


@index_page.route("/json_same")
def json_same():
    data = {"a": "b"}
    response = make_response(jsonify(data))
    return response


@index_page.route("/template")
def template():
    name = "Hello World"
    context = {"name": name}
    context['user'] = {"nickname": "IT1995", "qq": "570176391", "url": "www.it1995.cn"}
    context['num_list'] = [1, 2, 3, 4, 5]
    return render_template("index.html", **context)


@index_page.route('/', methods=['POST'])
def login():
    print(request.content_type)
    print(request.headers)
    username=request.get_json()['username']
    password=request.get_json()['password']
    print(username,password)
    result=sys_user.get_sys_user_by_username(username)
    # print(result.username,result.password)
    if result==None:
        return make_error_response(None,"用户名不存在")
    if result.password==password:
        data=sqlInit.query_to_dict(result)
        response=make_success_response(data,"欢迎登录")
        return response
    else:
        return make_error_response(None,"密码错误")


@index_page.route('/register', methods=['POST'])
def register():
    username=request.get_json()['username']
    password=request.get_json()['password']
    REAL_NAME = request.get_json()['REAL_NAME']
    SEX = request.get_json()['SEX']
    EMAIL = request.get_json()['EMAIL']
    PHONE = request.get_json()['PHONE']
    MOBILE = request.get_json()['MOBILE']
    DESCRIPTION = request.get_json()['DESCRIPTION']
    ISACTIVE='active'
    CREATEBY=0
    print(username,password)
    result=sys_user.get_sys_user_by_username(username)
    # print(result.password)
    if result!=None:
        return make_error_response(None,"用户名已存在")
    result=sys_user.add_sys_user(username,password,REAL_NAME,SEX,EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATEBY,0)
    if result==True:
        return make_success_response(None,"注册成功")
    else:
        return  make_error_response(None,"注册失败")


@index_page.route('/getSysUser', methods=['GET'])
def get_sys_user():
    ID=int(request.args.get("ID"))
    re=sys_user.get_sys_user_by_id(ID)
    result=sqlInit.query_to_dict(re)
    result['CREATED']=str(result['CREATED'])
    result['UPDATED']=str(result['UPDATED'])
    return make_success_response(result,"success")

@index_page.route('/updateSysUser', methods=['POST'])
def update_sys_user():
    ID=request.form['ID']
    username=request.form['username']
    REAL_NAME = request.form['REAL_NAME']
    SEX = request.form['SEX']
    EMAIL = request.form['EMAIL']
    PHONE = request.form['PHONE']
    MOBILE = request.form['MOBILE']
    DESCRIPTION = request.form['DESCRIPTION']
    UPDATEBY = request.form['UPDATEBY']
    ISACTIVE='active'
    re=sys_user.update_sys_user_by_id(ID,username,REAL_NAME,SEX,EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,UPDATEBY,0)
    if re==True:
        result=sqlInit.query_to_dict(sys_user.get_sys_user_by_username(username))
        return make_success_response(result,"更改成功")
    else:
        result=sqlInit.query_to_dict(sys_user.get_sys_user_by_id(ID))
        return make_error_response(result,'用户名已存在')

@index_page.route('/updateSysUserPassword', methods=['POST'])
def update_sys_user_password():
    ID=request.form['ID']
    old_password=request.form['pre_pass']
    new_password=request.form['new_pass']
    re=sys_user.update_sys_user_password_by_id(ID,old_password,new_password)
    if re==0:
        return make_success_response(None,"更改成功")
    elif re==1:
        return make_error_response(None,'密码错误')
    else:
        return make_error_response(None,'error')

# oldperson APIs
@index_page.route('/getOldPersonList', methods=['GET'])
def get_old_person_list():
    page=int(request.values.get("pageNow"))
    pagesize=int(request.values.get("pageSize"))
    content=request.values.get("content")
    persons=[]
    count=0
    if content==None:
        olds = oldperson_info.get_old_person_info_list(page, pagesize, content)
        count = oldperson_info.get_old_person_info_count(content)
        print(olds)
        persons=sqlInit.query_to_dict(olds)
    else:
        if util.is_number(content):
            olds = oldperson_info.get_old_person_info_by_id(content)
            count = oldperson_info.get_old_person_info_count_by_id(content)
            persons = sqlInit.query_to_dict(olds)
        else:
            # old=oldperson_info.get_old_person_info_by_name(content)
            # if old!=None:
            #     persons.append(sqlInit.query_to_dict(old))
            #     count=1
            olds = oldperson_info.get_old_person_info_list(page, pagesize, content)
            count = oldperson_info.get_old_person_info_count(content)
            persons = sqlInit.query_to_dict(olds)
    print(persons)
    for i in range(len(persons)):
        persons[i]['birthday']=str(persons[i]['birthday'])
        persons[i]['checkin_date']=str(persons[i]['checkin_date'])
        persons[i]['checkout_date']=str(persons[i]['checkout_date'])
        persons[i]['CREATED']=str(persons[i]['CREATED'])
        persons[i]['UPDATED']=str(persons[i]['UPDATED'])
    data={}
    data['olds']=persons
    data['total']=count
    print(data)
    return make_success_response(data,"success")

@index_page.route('/addOldPerson', methods=['POST'])
def add_old_person():

    username=request.get_json()['form'].get("username")
    gender=request.get_json()['form'].get("gender")
    phone=request.get_json()['form'].get("phone")
    id_card=request.get_json()['form'].get("id_card")
    birthday=request.get_json()['form'].get("birthday")
    checkin_date=request.get_json()['form'].get("checkin_date")
    checkout_date = request.get_json()['form'].get("checkout_date")
    room_number=request.get_json()['form'].get("room_number")
    firstguardian_phone = request.get_json()['form'].get("firstguardian_phone")
    firstguardian_name = request.get_json()['form'].get("firstguardian_name")
    firstguardian_relationship = request.get_json()['form'].get("firstguardian_relationship")
    firstguardian_wechat = request.get_json()['form'].get("firstguardian_wechat")
    secondguardian_phone = request.get_json()['form'].get("secondguardian_phone")
    secondguardian_name = request.get_json()['form'].get("secondguardian_name")
    secondguardian_relationship = request.get_json()['form'].get("secondguardian_relationship")
    secondguardian_wechat = request.get_json()['form'].get("secondguardian_wechat")
    DESCRIPTION=request.get_json()['form'].get("DESCRIPTION")
    health_state = request.get_json()['form'].get("health_state")
    CREATEBY = request.get_json()['form'].get("CREATEBY")

    REMOVE=0
    re=oldperson_info.add_old_person_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,
                                          "",id_card+".jpg",room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
                                          secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state,DESCRIPTION,CREATEBY)
    print(re)
    if re!=None:
        return make_success_response(re,"添加成功 ")
    else:
        return make_error_response(None,"添加失败")


@index_page.route('/updateOldPerson', methods=['POST'])
def update_old_person():
    print(request.get_json())
    ID=request.get_json()['elder'].get("ID")
    username=request.get_json()['elder'].get("username")
    gender=request.get_json()['elder'].get("gender")
    phone=request.get_json()['elder'].get("phone")
    id_card=request.get_json()['elder'].get("id_card")
    birthday=request.get_json()['elder'].get("birthday")
    checkin_date=request.get_json()['elder'].get("checkin_date")
    checkout_date = request.get_json()['elder'].get("checkout_date")
    room_number=request.get_json()['elder'].get("room_number")
    firstguardian_phone = request.get_json()['elder'].get("firstguardian_phone")
    firstguardian_name = request.get_json()['elder'].get("firstguardian_name")
    firstguardian_relationship = request.get_json()['elder'].get("firstguardian_relationship")
    firstguardian_wechat = request.get_json()['elder'].get("firstguardian_wechat")
    secondguardian_phone = request.get_json()['elder'].get("secondguardian_phone")
    secondguardian_name = request.get_json()['elder'].get("secondguardian_name")
    secondguardian_relationship = request.get_json()['elder'].get("secondguardian_relationship")
    secondguardian_wechat = request.get_json()['elder'].get("secondguardian_wechat")
    DESCRIPTION=request.get_json()['elder'].get("DESCRIPTION")
    health_state = request.get_json()['elder'].get("health_state")
    UPDATEBY = request.get_json()['elder'].get("UPDATEBY")
    REMOVE=0
    re=oldperson_info.update_oldperson_info_by_id(ID,username,gender,phone,id_card,birthday,checkin_date,checkout_date,
                                          "",id_card+".jpg",room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
                                          secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state,DESCRIPTION,UPDATEBY)

    return make_success_response(None,"添加成功 ")


@index_page.route('/deleteOldPerson', methods=['GET','POST'])
def delete_old_person():
    print(request.get_json())
    id=request.get_json().get('ID')
    UPDATEBY=request.get_json().get('UPDATEBY')
    re=oldperson_info.delete_old_person_info_by_id(id,UPDATEBY)
    if re==True:
        return make_success_response(None,"删除成功 ")
    else:
        return make_error_response(None,'删除失败')
@index_page.route('/getOldPersonSex', methods=['GET'])
def get_old_person_sex():
    male=oldperson_info.get_old_person_count_by_gender('m')
    female=oldperson_info.get_old_person_count_by_gender('f')
    return make_success_response({'male':male,'female':female},"success")

@index_page.route('/countOldPerson', methods=['GET'])
def count_old_person():
    olds = oldperson_info.get_old_person_info_list(1, 9999999, None)
    print(olds)
    persons=sqlInit.query_to_dict(olds)
    distributed=[0,0,0,0,0,0]
    for item in persons:
        age=util.getAge(item['birthday'])
        if age<60:
            distributed[0]=distributed[0]+1
        elif age>=60 and age<65:
            distributed[1]=distributed[1]+1
        elif age>=65 and age<70:
            distributed[2]=distributed[2]+1
        elif age>=70 and age<75:
            distributed[3]=distributed[3]+1
        elif age>=75 and age<80:
            distributed[4]=distributed[4]+1
        else:
            distributed[5]=distributed[5]+1
    print(distributed)
    return make_success_response(distributed,"success ")


# employee APIS
@index_page.route('/getEmployeeList', methods=['GET'])
def get_employee_list():
    page=int(request.values.get("pageNow"))
    pagesize=int(request.values.get("pageSize"))
    content=request.values.get("content")
    persons=[]
    count=0

    if content==None:
        employees = employee_info.get_employee_info_list(page, pagesize, content)
        count = employee_info.get_employee_count(content)
        persons=sqlInit.query_to_dict( employees)
    else:
        if util.is_number(content):
            employees = employee_info.get_employee_info_by_id(content)
            count = 1
            person = sqlInit.query_to_dict(employees)
            persons.append(person)
        else:
            # old=employee_info.get_employee_info_by_name(content)
            # if old!=None:
            #     persons.append(sqlInit.query_to_dict(old))
            #     count=1
            employees = employee_info.get_employee_info_list(page, pagesize, content)
            count = employee_info.get_employee_count(content)
            persons = sqlInit.query_to_dict(employees)
    for i in range(len(persons)):
        print(persons)
        persons[i]['birthday']=str(persons[i]['birthday'])
        persons[i]['hire_date']=str(persons[i]['hire_date'])
        persons[i]['resign_date']=str(persons[i]['resign_date'])
        persons[i]['CREATED']=str(persons[i]['CREATED'])
        persons[i]['UPDATED']=str(persons[i]['UPDATED'])
    data={}
    data['employees']=persons
    data['total']=count
    print(data)
    return make_success_response(data,"success")

@index_page.route('/addEmployee', methods=['POST'])
def add_employee():
    username=request.get_json()['form'].get("username")
    gender=request.get_json()['form'].get("gender")
    phone=request.get_json()['form'].get("phone")
    id_card=request.get_json()['form'].get("id_card")
    birthday=request.get_json()['form'].get("birthday")
    hire_date=request.get_json()['form'].get("hire_date")
    # resign_date = request.get_json()['form'].get("resign_date")
    DESCRIPTION=request.get_json()['form'].get("DESCRIPTION")
    CREATEBY=request.get_json()['form'].get("CREATEBY")
    re=employee_info.add_employee_info(username,gender,phone,id_card,birthday,hire_date,id_card+".jpg",DESCRIPTION,'active',CREATEBY)
    if re!=None:
        return make_success_response(re,"添加成功 ")
    else:
        return make_error_response(None,"添加失败")



@index_page.route('/updateEmployee', methods=['POST'])
def update_employee():
    id=request.get_json()['form'].get("id")
    username=request.get_json()['form'].get("username")
    gender=request.get_json()['form'].get("gender")
    phone=request.get_json()['form'].get("phone")
    id_card=request.get_json()['form'].get("id_card")
    birthday=request.get_json()['form'].get("birthday")
    hire_date=request.get_json()['form'].get("hire_date")
    # resign_date = request.get_json()['form'].get("resign_date")
    DESCRIPTION=request.get_json()['form'].get("DESCRIPTION")
    UPDATEBY=request.get_json()['form'].get("UPDATEBY")
    re=employee_info.update_employee_info_by_id(id,username,gender,phone,id_card,birthday,hire_date,DESCRIPTION,UPDATEBY)
    return make_success_response(None,"修改成功")


@index_page.route('/deleteEmployee', methods=['GET','POST'])
def delete_employee():
    id=request.get_json().get('id')
    UPDATEBY=request.get_json().get('UPDATEBY')
    re=employee_info.delete_employee_info_by_id(id,UPDATEBY)
    if re==True:
        return make_success_response(None,"删除成功 ")
    else:
        return make_error_response(None,'删除失败')

@index_page.route('/getEmployeeSex', methods=['GET'])
def get_employee_sex():
    male=employee_info.get_employee_count_by_gender('m')
    female=employee_info.get_employee_count_by_gender('f')
    return make_success_response({'male':male,'female':female},"success")

@index_page.route('/countEmployee', methods=['GET'])
def count_employee():
    employees = employee_info.get_employee_info_list(1, 9999999, None)
    persons=sqlInit.query_to_dict(employees)
    distributed=[0,0,0,0,0]
    for item in persons:
        age=util.getAge(item['birthday'])
        if age<30:
            distributed[0]=distributed[0]+1
        elif age>=30 and age<40:
            distributed[1]=distributed[1]+1
        elif age>=40 and age<50:
            distributed[2]=distributed[2]+1
        elif age>=50 and age<60:
            distributed[3]=distributed[3]+1
        else:
            distributed[4]=distributed[4]+1
    print(distributed)
    return make_success_response(distributed,"success ")

# volunteer APIS
@index_page.route('/getVolunteerList', methods=['GET'])
def get_volunteer_list():
    page=int(request.values.get("pageNow"))
    pagesize=int(request.values.get("pageSize"))
    content=request.values.get("content")
    persons=[]
    count=0
    if content==None:
        volunteers = volunteer_info.get_volunterr_info_list(page, pagesize, content)
        count = volunteer_info.get_volunterr_info_count(content)
        persons=sqlInit.query_to_dict(volunteers)
    else:
        if util.is_number(content):
            volunteers = volunteer_info.get_volunteer_info_by_id(content)
            count = 1
            person = sqlInit.query_to_dict(volunteers)
            persons.append(person)
        else:
            # old=volunteer_info.get_volunteer_info_by_name(content)
            # if old!=None:
            #     persons.append(sqlInit.query_to_dict(old))
            #     count=1
            volunteers = volunteer_info.get_volunterr_info_list(page, pagesize, content)
            count = volunteer_info.get_volunterr_info_count(content)
            persons = sqlInit.query_to_dict(volunteers)
    for i in range(len(persons)):
        persons[i]['birthday']=str(persons[i]['birthday'])
        persons[i]['checkin_date']=str(persons[i]['checkin_date'])
        persons[i]['checkout_date']=str(persons[i]['checkout_date'])
        persons[i]['CREATED']=str(persons[i]['CREATED'])
        persons[i]['UPDATED']=str(persons[i]['UPDATED'])
    data={}
    data['volunteers']=persons
    data['total']=count
    return make_success_response(data,"success")

@index_page.route('/addVolunteer', methods=['POST'])
def add_volunteer():

    name=request.get_json()['form'].get("name")
    gender=request.get_json()['form'].get("gender")
    phone=request.get_json()['form'].get("phone")
    id_card=request.get_json()['form'].get("id_card")
    birthday=request.get_json()['form'].get("birthday")
    checkin_date=request.get_json()['form'].get("checkin_date")
    # resign_date = request.get_json()['form'].get("resign_date")
    DESCRIPTION=request.get_json()['form'].get("DESCRIPTION")
    CREATEBY=request.get_json()['form'].get("CREATEBY")
    print(CREATEBY)
    re=volunteer_info.add_volunteer_info(name,gender,phone,id_card,birthday,checkin_date,DESCRIPTION,CREATEBY)
    if re!=None:
        return make_success_response(re,"添加成功 ")
    else:
        return make_error_response(None,"添加失败")



@index_page.route('/updateVolunteer', methods=['POST'])
def update_volunteer():
    id=request.get_json()['form'].get("id")
    username=request.get_json()['form'].get("name")
    gender=request.get_json()['form'].get("gender")
    phone=request.get_json()['form'].get("phone")
    id_card=request.get_json()['form'].get("id_card")
    birthday=request.get_json()['form'].get("birthday")
    checkin_date=request.get_json()['form'].get("checkin_date")
    checkout_date = request.get_json()['form'].get("checkout_date")
    DESCRIPTION=request.get_json()['form'].get("DESCRIPTION")
    UPDATEBY=request.get_json()['form'].get("UPDATEBY")
    re=volunteer_info.update_volunteer_info_by_id(id,username,gender,phone,id_card,birthday,checkin_date,checkout_date,DESCRIPTION,UPDATEBY)
    print(re)
    return make_success_response(None,"修改成功")


@index_page.route('/deleteVolunteer', methods=['GET','POST'])
def delete_volunteer():
    id=request.get_json().get('id')
    UPDATEBY=request.get_json().get('UPDATEBY')
    re=volunteer_info.delete_volunteer_info_by_id(id,UPDATEBY)
    if re==True:
        return make_success_response(None,"删除成功 ")
    else:
        return make_error_response(None,'删除失败')
@index_page.route('/getVolunteerSex', methods=['GET'])
def get_volunteer_sex():
    male=volunteer_info.get_volunteer_count_by_gender('m')
    female=volunteer_info.get_volunteer_count_by_gender('f')
    return make_success_response({'male':male,'female':female},"success")

@index_page.route('/countVolunteer', methods=['GET'])
def count_volunteer():
    volunteers = volunteer_info.get_volunterr_info_list(1, 9999999, None)
    persons=sqlInit.query_to_dict(volunteers)
    distributed=[0,0,0,0,0]
    for item in persons:
        age=util.getAge(item['birthday'])
        if age<30:
            distributed[0]=distributed[0]+1
        elif age>=30 and age<40:
            distributed[1]=distributed[1]+1
        elif age>=40 and age<50:
            distributed[2]=distributed[2]+1
        elif age>=50 and age<60:
            distributed[3]=distributed[3]+1
        else:
            distributed[4]=distributed[4]+1
    print(distributed)
    return make_success_response(distributed,"success ")


# event APIs
@index_page.route('/getEventList', methods=['POST'])
def get_event_list():
    print(request.form)
    event_type=request.form.get('type')
    event_location=request.form.get('location')
    event_date=request.form.get('date')
    event_desc=request.form.get('desc')
    oldperson_id=request.form.get('old_id')
    page=int(request.form.get("pageNow"))
    pagesize=int(request.form.get("pageSize"))
    criteria={}

    if event_type!='':
        criteria['event_type']=int(event_type)
    if event_date!='':
        criteria['event_date']=event_date
    if event_location!='':
        criteria['event_location']=event_location
    if event_desc!='':
        criteria['event_desc']=event_desc
    if oldperson_id!='':
        criteria['oldperson_id']=oldperson_id
    re=event_info.get_event_info_list(page,pagesize,criteria)
    total=event_info.get_event_info_count(criteria)
    result=sqlInit.query_to_dict(re)
    for i in range(len(result)):
        result[i]['id']=i+1+(page-1)*pagesize
        result[i]['event_date']=str(result[i]['event_date'])
        result[i]['event_type']=events[result[i]['event_type']-1]

    data={}
    data['total']=total
    data['events']=result
    if re!=None:
        return make_success_response(data,"success")
    else:
        return make_error_response(None,'error')




# cv APIs
@index_page.route('/getProfilePhoto', methods=['POST'])
def get_profile_photo():
    ID=int(request.args.get("ID"))
    re=sys_user.get_sys_user_by_id(ID)
    result=sqlInit.query_to_dict(re)
    return make_success_response(result,"success")

@index_page.route('/addEvent', methods=['POST'])
def add_event():
    # ID=int(request.args.get("ID"))
    # re=sys_user.get_sys_user_by_id(ID)
    event_type=int(request.form.get('event_type'))
    event_date=request.form.get('event_date')
    event_location=request.form.get('event_location')
    event_desc=request.form.get('event_desc')
    oldperson_id=request.form.get('oldperson_id')
    img_dir=request.form.get('img_dir')
    re=event_info.add_event_info(event_type,event_date,event_location,event_desc,oldperson_id,img_dir)
    print(re)
    if re==True:
        return make_success_response(None,"success")
    else: 
        return make_error_response(None,'failed')


@index_page.route('/countTotal', methods=['GET'])
def count_total():
    data={}
    results=[]
    now = datetime.now()
    for i in range(7):
        result={}
        result['v_date']=now.strftime("%Y-%m-%d")
        print(result['v_date'])
        zeroToday= now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
        lastToday = zeroToday + timedelta(hours=23, minutes=59, seconds=59)  
        result['c_old']=oldperson_info.get_old_person_checkin_count_by_day(zeroToday,lastToday)
        result['l_old']=oldperson_info.get_old_person_checkout_count_by_day(zeroToday,lastToday)
        result['c_employee']=employee_info.get_employee_hire_count_by_day(zeroToday,lastToday)
        result['l_employee']=employee_info.get_employee_resign_count_by_day(zeroToday,lastToday)
        result['c_volu']=volunteer_info.get_volunteer_checkin_count_by_day(zeroToday,lastToday)
        result['l_volu']=volunteer_info.get_volunteer_checkout_count_by_day(zeroToday,lastToday)
        print(result['v_date'],result['c_old']) 
        now=now+timedelta(days=-1)
        results.append(result)
    data['old_total']=oldperson_info.get_old_person_info_count_by_remove(0)
    data['employee_total']=employee_info.get_employee_count_by_remove(0)
    data['volunteer_total']=volunteer_info.get_volunteer_count_by_remove(0)
    data['v_num']=results
    print(data)
    return make_success_response(data,"success")
    # return make_success_response(distributed,"success ")




@index_page.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        print(request.form)
        # name=request.values.get("name")
        name=request.form['name']
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, 'uploads/') + "%s" % (name)
        f.save(upload_path)
        return make_success_response(None,"success")


@index_page.route('/display/img/<string:filename>', methods=['GET'])
def display_img(filename):
    base_path = os.path.abspath(os.path.dirname(__file__))
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(
                base_path + '/uploads/' + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass
