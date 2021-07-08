from flask import Flask, Blueprint, request, make_response, jsonify, render_template
from dal import oldperson_info,sys_user,event_info,employee_info,volunteer_info
from common import sqlInit,redisInit
from common import util
import  os
index_page = Blueprint("index_page", __name__)


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

@index_page.route("/")
def text():
    return "text/html"


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


@index_page.route('/login', methods=['POST'])
def login():
    username=request.values.get("username")
    password=request.values.get("password")
    result=sys_user.get_sys_user_by_username(username)
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
    username=request.values.get("username")
    password=request.values.get("password")
    REAL_NAME = request.values.get("REAL_NAME")
    SEX = request.values.get("SEX")
    EMAIL = request.values.get("EMAIL")
    PHONE = request.values.get("PHONE")
    MOBILE = request.values.get("MOBILE")
    DESCRIPTION=""
    ISACTIVE='active'
    CREATEBY=REAL_NAME
    print(username,password)
    result=sys_user.get_sys_user_by_username(username)
    print(result.password)
    if result!=None:
        return make_error_response(None,"用户名已存在")
    result=sys_user.add_sys_user(username,password,REAL_NAME,SEX,EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATEBY,0)
    if result==True:
        return make_success_response(None,"注册成功")
    else:
        return  make_error_response(None,"注册失败")



@index_page.route('/getOldPersonList', methods=['POST'])
def get_old_person_list():
    page=int(request.values.get("page"))
    pagesize=int(request.values.get("pagesize"))
    content=request.values.get("content")
    persons=[]
    count=0
    if content=='':
        olds = oldperson_info.get_old_person_info_list(page, pagesize, content)
        count = oldperson_info.get_old_person_info_count(content)
        persons=sqlInit.query_to_dict(olds)
    else:
        if util.is_number(content):
            pass
        else:
            old=oldperson_info.get_old_person_info_by_id(content)
            if old!=None:
                persons.append(sqlInit.query_to_dict(old))
                count=1
            olds = oldperson_info.get_old_person_info_list(page, pagesize, content)
            count = oldperson_info.get_old_person_info_count(content)
            persons = sqlInit.query_to_dict(olds)
    data={}
    data['olds']=persons
    data['total']=count
    return make_success_response(data,"success")

@index_page.route('/addOldPerson', methods=['POST'])
def add_old_person():
    username=request.values.get("username")
    gender=request.values.get("gender")
    phone=request.values.get("phone")
    id_card=request.values.get("id_card")
    birthday=request.values.get("birthday")
    checkin_date=request.values.get("checkin_date")
    checkout_date = request.values.get("checkout_date")
    room_number=request.values.get("room_number")
    firstguardian_phone = request.values.get("firstguardian_phone")
    firstguardian_name = request.values.get("firstguardian_name")
    firstguardian_relationship = request.values.get("firstguardian_relationship")
    firstguardian_wechat = request.values.get("firstguardian_wechat")
    secondguardian_phone = request.values.get("secondguardian_phone")
    secondguardian_name = request.values.get("secondguardian_name")
    secondguardian_relationship = request.values.get("secondguardian_relationship")
    secondguardian_wechat = request.values.get("secondguardian_wechat")
    health_state = request.values.get("health_state")
    CREATEBY = request.values.get("CREATEBY")
    UPDATEBY = request.values.get("UPDATEBY")
    REMOVE=0

    re=oldperson_info.add_old_person_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,
                                          "",username+"avatar.jpg",room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
                                          secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state)

    return make_success_response(None,"添加成功 ")


@index_page.route('/deleteOldPerson', methods=['POST'])
def delete_old_person():
    username=request.values.get("username")
    gender=request.values.get("gender")
    phone=request.values.get("phone")
    id_card=request.values.get("id_card")
    birthday=request.values.get("birthday")
    checkin_date=request.values.get("checkin_date")
    checkout_date = request.values.get("checkout_date")
    room_number=request.values.get("room_number")
    firstguardian_phone = request.values.get("firstguardian_phone")
    firstguardian_name = request.values.get("firstguardian_name")
    firstguardian_relationship = request.values.get("firstguardian_relationship")
    firstguardian_wechat = request.values.get("firstguardian_wechat")
    secondguardian_phone = request.values.get("secondguardian_phone")
    secondguardian_name = request.values.get("secondguardian_name")
    secondguardian_relationship = request.values.get("secondguardian_relationship")
    secondguardian_wechat = request.values.get("secondguardian_wechat")
    health_state = request.values.get("health_state")
    CREATEBY = request.values.get("CREATEBY")
    UPDATEBY = request.values.get("UPDATEBY")
    REMOVE=0

    re=oldperson_info.add_old_person_info(username,gender,phone,id_card,birthday,checkin_date,checkout_date,
                                          "",username+"avatar.jpg",room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
                                          secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,health_state)

    return make_success_response(None,"添加成功 ")


# @index_page.route('/getSysUserList', methods=['GET'])
# def get_sys_user_list():
#     page=request.values.get("page")
#     pagesize=request.values.get("pagesize")
#     username=request.values.get("username")
#     criteria={}
#     if username!='':
#         criteria['username']=username
#     users=oldperson_info.get_old_person_info_list(page,pagesize,criteria)
#     total=oldperson_info.get_old_person_info_count(criteria)
#     data={}
#     data['olds']=sqlInit.query_to_dict(olds)
#     data['total']=total
#     return make_success_response(data,"success")

@index_page.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        name=request.values.get("name")
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, 'static\\uploads\\') + "%s" % (name)
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
                base_path + '/static/uploads/' + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass
