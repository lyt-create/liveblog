
# author:lytcreate
# blog:liveblog
# website:http://www.liveblog.cn
# powered by Django


import datetime
import pymysql
from django.conf import settings
from liveblog.settings import DATABASES
host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']
user = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
database = DATABASES['default']['NAME']

def datas(request):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select count(*) from liveblog_say")
    dt = cursor.fetchone()
    cursor.execute('select count(*) from liveblog_dailyrecord')
    rz = cursor.fetchone()
    cursor.execute('select count(*) from liveblog_comments')
    pl = cursor.fetchone()
    cursor.execute('select sum(viewsnumber) from liveblog_dailyrecord')
    ll = cursor.fetchone()
    cursor.execute('select sum(likesnumber) from liveblog_dailyrecord')
    dz = cursor.fetchone()
    cursor.execute("select username from liveblog_myuser where id=1")
    admin = cursor.fetchone()
    date = datetime.datetime.now()
    cursor.execute("select signs,headimage,weibo,wechat,QQ,email,username from liveblog_myuser where id = 1")
    person = cursor.fetchone()
    cursor.close()
    cursors = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursors.execute("select * from liveblog_links")
    links_list = cursors.fetchall()
    cursors.close()
    conn.close()

    return {'dt':dt,'rz':rz,'pl':pl,'ll':ll,'dz':dz,'admin':admin,'date':date,'links_list':links_list,'person':person}