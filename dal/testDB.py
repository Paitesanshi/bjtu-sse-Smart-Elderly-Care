import oldperson_info
import time
#sys_user.update_sys_user_by_id(1,"wl","zxc110","王磊123","male","18301107@bjtu.edu.cn","54321","13088866688","","",0,0)
# results=sys_user.get_sys_user_info_list(1,20,"王")
# result=sys_user.get_sys_user_count("王")
# print(results)
# print(result)
# result=oldperson_info.get_old_person_info_list(1,20,"")
# print(result[0].username)

re=oldperson_info.add_old_person_info("wll","male","13031170798","111111111111111111",time.strftime("%Y-%m-%d", time.localtime()),time.strftime("%Y-%m-%d", time.localtime()),time.strftime("%Y-%m-%d", time.localtime()),
                                 "","","303","wlll","父子","111111111111","123321","wllll","母子","12332112365","1232111","healthy")
print(re)
# re=oldperson_info.delete_old_person_info_by_id(17)