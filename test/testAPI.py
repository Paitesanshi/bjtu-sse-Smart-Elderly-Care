import re

from flask import Flask
import requests


url1 = 'https://www.jianshu.com/u/39cef8a56bf9'
url = 'http://121.196.111.9:5000/secs/addEvent'
data = {'authenticity_token': '+gy/zbvCNJATHwvygafFlOOR4gF5dl3bzheFlArNlN3IvlSuURRTZYbFZ5wTAdIwWl+TaykOF+lXbwQXWYkodg==',
        'user[email]': '123456789@qq.com',
        'user[password]': '123456789',
        'user[remember_me]': '0',
        'commit': '登录'}

def post_assert(url, data):
    # 判断url是否合法，需要了解url的构成，用正则匹配进行判断
    # url的构成：协议、域名、端口、虚拟目录、文件名、参数部分等  其中：协议、域名是必须存在的
    # 协议为：http或https  域名为：xxx.xxxx.xxx 端口为：数字
    if not re.match(r'^https?://[^\s]*\.[^\s]*\.[com|cn|net].*', url):
        return 'URL不合法，无法执行接口用例'
    r = requests.post(url, data=data)
    r.encoding = 'utf-8'
    if r.status_code == 200:
        return True
    else:
        return r.text