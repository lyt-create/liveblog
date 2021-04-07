# author:lytcreate
# blog:liveblog
# website:http://www.liveblog.cn
# powered by Django

import datetime
import json
import random

import pymysql
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from liveblog import models
from liveblog.models import Pictures, Photos, Say, Dailyrecord, Goals, Files, Myuser
from liveblog.settings import EMAIL_HOST_USER,DATABASES

host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']
user = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
database = DATABASES['default']['NAME']
adminsite = Myuser.objects.get(id=1)
website = adminsite.website
adminemail = adminsite.email

def login(request):
    if request.method == 'GET':
        next = request.GET.get('next')
        if next == None:
            next = 'home.html'
        return render(request, 'login.html',{'next':next})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST.get('next')
        if next == '':
            next = 'home.html'
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session.set_expiry(60 * 60) #60分钟后失效
            return redirect(next)
        else:
            tishi='账号或密码错误，请检查用户名或密码！'
            return render(request,'login.html',{'tishi':tishi})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home.html')

# def register(request):
#     if request.method == 'GET':
#         username =''
#         password=''
#         email=''
#         yzm = '获取验证码'
#         return render(request,'register.html',{'username':username,'password':password,'email':email,'yzm':yzm})
#     else:
#         name = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         yanzhengma = request.POST.get('yanzhengma')
#         yzm = '获取验证码'
#         user = User.objects.filter(username=name)
#         mail = User.objects.filter(email=email)
#         if not user:
#             if not mail:
#                 if yanzhengma == request.session.get('VCode'):
#                     User.objects.create_user(username=name, password=password, email=email)
#                     return redirect("/login.html")
#                 else:
#                     tishi = '验证码错误，请重新获取验证码！'
#                     return render(request,'register.html',{'tishi':tishi,'username':name,'password':password,'email':email,'yzm':yzm})
#             else:
#                 tishi = '这个邮箱已经被别人占用咯，重新选一个吧！'
#                 return render(request, 'register.html',
#                               {'tishi': tishi, 'username': name, 'password': password, 'email': email, 'yzm': yzm})
#         # 此处的User 是 django 自带的model
#         else:
#             tishi = '用户名已存在，请重新输入一个有趣的名字吧！'
#             return render(request,'register.html',{'tishi':tishi,'username':name,'password':password,'email':email,'yzm':yzm})
#
#
# def registers(request):
#     if request.method == 'GET':
#         yzm = '获取验证码'
#         return render(request,'register.html',{'yzm':yzm})
#     else:
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         email = request.POST.get("email")
#         if email =='':
#             tishi = '邮箱不能为空！'
#             yzm = '获取验证码'
#             return render(request, 'register.html',
#                           {'username': username, 'password': password, 'email': email, 'yzm': yzm,'tishi':tishi})
#         # print(email)
#         else:
#             zccode = str(random.randint(000000, 999999))
#             request.session['VCode'] = zccode
#             send_mail('Liveblog注册验证码', '这是您的注册验证码：' + zccode + ',如果不是本人注册请忽略此条信息！人生若只如初见，Liveblog伴您记录美好时光！',
#                       'liveblog@qq.com',
#                       [email], fail_silently=False)
#             yzm = '验证码已发'
#             return render(request, 'register.html',
#                           {'username': username, 'password': password, 'email': email, 'yzm': yzm})

def home(request):
    if request.method == 'GET':
        home = Dailyrecord.objects.all().order_by('-publicationdate')
        pagenitor = Paginator(home, 5)
        # page_num = pagenitor.num_pages
        curuent_page_num = int(request.GET.get('page', 1))
        curuent_page = pagenitor.page(curuent_page_num)
        return render(request,'home.html',{'curuent_page':curuent_page})
    return render(request,'home.html')

def saying(request):
    if request.method == 'GET':

        say = Say.objects.all().order_by('-publicationdate')
        pagenitor = Paginator(say, 7)
        # page_num = pagenitor.num_pages
        curuent_page_num = int(request.GET.get('page',1))
        curuent_page = pagenitor.page(curuent_page_num)
        err = 0
        return render(request,'saying.html',{'curuent_page':curuent_page,'err':err})
    else:
        contents = request.POST.get('contents')

        if contents == '':
            err = 1
            conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                   charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("select * from liveblog_say order by publicationdate desc limit 7")
            say_list = cursor.fetchall()
            cursor.close()
            conn.close()

            return render(request,'saying.html',{'err':err,'say_list':say_list})
        else:
            conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                   charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(
                "insert into liveblog_say(publisherid,contents,viewsnumber,comments,likesnumber,publicationdate) values (%s,%s,%s,%s,%s,%s)",
                ['1', contents, 0, 0, 0, datetime.datetime.now(), ])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('saying.html')

def album(request):
    if request.method == 'GET':
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from liveblog_pictures order by id desc limit 25")
        pic_list = cursor.fetchall()
        return render(request,'album.html',{'pic_list':pic_list})
    else:
        f = request.FILES.get('file')
        if f != None:
            f.name = 'liveblog-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.' + f.name.split('.')[1]
            if f.name.split('.')[-1] not in ['jpeg', 'jpg', 'png','JPEG','PNG','JPG'] or f == None:
                error = 1
                conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                       charset='utf8')
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cursor.execute("select * from liveblog_pictures order by id desc limit 25")
                pic_list = cursor.fetchall()
                return render(request, 'album.html', {'pic_list': pic_list, 'error': error})

            else:
                img = Pictures(
                    publisherid=request.user.id,
                    photos=f,
                    uploaddate=datetime.datetime.now()
                )
                img.save()
                return redirect('album.html')
        else:
            conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                   charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("select * from liveblog_pictures order by id desc limit 35")
            pic_list = cursor.fetchall()
            error = 1
            return render(request, 'album.html', {'pic_list': pic_list, 'error': error})



def motus(request):
    motus = Goals.objects.all().order_by('-state')
    pagenitor = Paginator(motus, 5)
    curuent_page_num = int(request.GET.get('page', 1))
    curuent_page = pagenitor.page(curuent_page_num)

    return render(request, 'motus.html', {'curuent_page': curuent_page})

def timeline(request):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from liveblog_dailyrecord order by publicationdate desc limit 10")
    timeline = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'timeline.html',{'timeline':timeline})

def timelines(request):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from liveblog_dailyrecord order by publicationdate desc")
    timeline = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'timeline.html', {'timeline': timeline})

def about(request):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select subject,content,time from liveblog_about where id=1")
    about = cursor.fetchone()
    return render(request,'about.html',{'about':about})

@login_required()
def updateabout(request):
    if request.method == "GET":
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select subject,content,time from liveblog_about where id=1")
        about = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request,'updateabout.html',{'about':about})
    else:
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select * from liveblog_about")
        resoult = cursor.fetchone()
        if resoult:
            cursor.execute("update liveblog_about set subject=%s,content=%s,time=%s where id=1",[subject,content,datetime.datetime.now()])
        else:
            cursor.execute("insert into liveblog_about(subject,content,time) values (%s,%s,%s)",[subject,content,datetime.datetime.now()])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('about.html')

def albums(request):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from liveblog_pictures order by id desc")
    pic_list = cursor.fetchall()
    return render(request, 'album.html', {'pic_list': pic_list})


@login_required
def publish(request):
    if request.method == 'GET':
        return render(request,'publish.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('pic')

        if file.name.split('.')[-1] in ['jpeg', 'jpg', 'png','JPEG','PNG','JPG']:
            daily = Dailyrecord(
                publisherid = 1,
                theme = title,
                contents = content,
                viewsnumber=1,
                comments=0,
                likesnumber=0,
                publicationdate=datetime.datetime.now(),
                image=file
                )
            daily.save()
            return redirect('home.html')
        else:
            return HttpResponse("封面图片格式错误！")


@csrf_exempt
@login_required()
def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file.name = 'liveblog-'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.'+file.name.split('.')[1]
        new_photos = Photos(
            photo=file,
            time=datetime.datetime.now()
        )
        new_photos.save()
        path = "media/images/"+file.name

        return JsonResponse(
            {
                "code": 0
                , "msg": ""
                , "data": {
                  "src": path
                , "title": ""
            }
            }
        )
    else:
        return HttpResponse("错误的请求")

def daily(request):
    if request.method == 'GET':
        read = request.GET.get('read')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select id from liveblog_dailyrecord order by id desc ")
        number = cursor.fetchone()
        cursor.execute("update liveblog_dailyrecord set viewsnumber=viewsnumber+1 where id=%s",[read])
        conn.commit()
        cursor.execute("select id,publisherid,theme,contents,viewsnumber,comments,likesnumber,publicationdate from liveblog_dailyrecord where id=%s",[read])
        daily_list = cursor.fetchone()
        if daily_list[0] < 2 :
            up = '没有上一篇了'
            ups = '#'
        else:
            for k in range(1,999):   #s删除日志小于999就可以，或者这里的上限可以确定为日志总条数
                cursor.execute("select theme from liveblog_dailyrecord where id =%s",[daily_list[0]-k])
                up_list = cursor.fetchone()
                if up_list:
                    up = up_list[0]
                    ups = int(daily_list[0]-k)
                    break
        if daily_list[0]+1 > number[0]:
            down = '没有下一篇了'
            downs = '#'
        else:
            for j in range(1, 999):
                cursor.execute("select theme from liveblog_dailyrecord where id=%s",[daily_list[0]+j])  
                down_list = cursor.fetchone()

                if down_list:
                    down = down_list[0]
                    downs = int(daily_list[0]+j)
                    break

        cursor.close()
        cursors = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursors.execute("select * from liveblog_comments where articleid=%s order by publicationdate desc ",[read])
        com_list = cursors.fetchall()
        for i in range(0,len(com_list)):
            com_list[i]['pic'] = random.randint(0,9)

        cursors.close()
        conn.close()
        return render(request,'daily.html',{'daily_list':daily_list,'up':up,'down':down,'ups':ups,'downs':downs,'com_list':com_list})
    else:
        name = request.POST.get('name')
        comments = request.POST.get('comments')
        did = request.POST.get('did')
        mail = request.POST.get('mail')
        if '@' not in mail:
            mail = 'liveblog@qq.com'
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            "insert into liveblog_comments(articleid,username,content,publicationdate,dadid,dadname,email) values (%s,%s,%s,%s,%s,%s,%s)",
            [did, name, comments, datetime.datetime.now(), 0, 0, mail])
        conn.commit()
        cursor.execute("select theme from liveblog_dailyrecord where id=%s",[did])
        art = cursor.fetchone()
        cursor.execute("update liveblog_dailyrecord set comments=comments+1 where id=%s",[did])
        conn.commit()
        cursor.close()
        conn.close()
        send_mail('Liveblog新评论提醒', '您的文章《'+art[0]+'》被  '+name+'  评论了！，快去看看吧：'+website+'/daily.html?read='+did, EMAIL_HOST_USER,
                  [adminemail], fail_silently=True)
        next = 'daily.html?read=' + did
        return redirect(next)


def publishcomments(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        ucomments = request.POST.get('ucomments')
        articleid = request.POST.get('articleid')
        dadid = request.POST.get('dadid')
        dadname = request.POST.get('dadname')
        uemail = request.POST.get('uemail')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("insert into liveblog_comments(articleid,username,content,publicationdate,dadid,dadname,email) values (%s,%s,%s,%s,%s,%s,%s)",[articleid,uname,ucomments,datetime.datetime.now(),dadid,dadname,uemail])
        conn.commit()
        cursor.execute("select theme from liveblog_dailyrecord where id=%s",[articleid])
        art = cursor.fetchone()
        cursor.execute("select username,email from liveblog_comments where id = %s",[dadid])
        ste = cursor.fetchone()
        cursor.close()
        conn.close()
        send_mail('Liveblog的评论被评论提醒', ste[0]+',您在文章《' + art[0] + '》中的评论被  ' + uname + '  评论了！，快去看看吧：' + website + '/daily.html?read=' + articleid,
                  EMAIL_HOST_USER,
                  [ste[1]], fail_silently=True)
        return redirect('daily.html?read='+articleid)
    else:
        return redirect('home.html')


@csrf_exempt
def updatesaylike(request):
    id = request.POST.get('id')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("update liveblog_say set likesnumber=likesnumber+1 where id=%s",[id])
    conn.commit()
    cursor.execute("select likesnumber from liveblog_say where id=%s",[id])
    like = cursor.fetchone()
    cursor.close()
    conn.close()
    data = {}
    data['id']= id
    data['likes'] = like[0]

    return HttpResponse(json.dumps(data))

@csrf_exempt
def dailylikes(request):
    id = request.GET.get('id')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("update liveblog_dailyrecord set likesnumber=likesnumber+1 where id=%s",[id])
    conn.commit()
    cursor.execute("select likesnumber from liveblog_dailyrecord where id=%s",[id])
    data=cursor.fetchone()
    cursor.close()
    conn.close()
    return HttpResponse(data)

@login_required
def writemotus(request):
    if request.method == 'GET':
        return render(request,'writemotus.html')
    else:
        title = request.POST.get('title')
        time = request.POST.get('time')
        content = request.POST.get('content')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("insert into liveblog_goals(theme,contents,state,successdate) values (%s,%s,%s,%s)",[title,content,'进行中',time])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('motus.html')

@login_required
def motussuccess(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("update liveblog_goals set state='已完成' where id=%s",[nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('motus.html')

@login_required
def editdaily(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select id,theme,contents,image from liveblog_dailyrecord where id=%s",[nid])
        edit_list = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request,'publish.html',{'edit_list':edit_list})
    else:
        id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('pic')
        if file:
            file.name = random.choice('liveblog')+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.'+file.name.split('.')[1]
        else:
            file = request.POST.get('ypic')

        print(file)

        daily = Dailyrecord.objects.get(id=id)
        daily.theme = title
        daily.contents = content
        daily.publicationdate = datetime.datetime.now()
        daily.image = file
        daily.save()
        return redirect('daily.html?read='+id)

@login_required
def editlinks(request):
    if request.method == 'GET':
        return render(request,'updateabout.html')
    else:
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("insert into liveblog_links(webname ,website) values (%s,%s)",[subject,content])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('home.html')

@login_required
def deldaily(request):
    id = request.GET.get('nid')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("delete from liveblog_dailyrecord where id=%s ",[id])
    conn.commit()
    cursor.execute("delete from liveblog_comments where articleid=%s",[id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('home.html')

@login_required
def editsaying(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select id,contents from liveblog_say where id=%s",[nid])
        say = cursor.fetchone()
        cursor.close()
        cursors = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursors.execute("select * from liveblog_say order by publicationdate desc limit 7")
        say_list = cursors.fetchall()
        cursors.close()
        conn.close()
        return render(request,'saying.html',{'say':say,'say_list':say_list})
    else:
        id = request.POST.get('id')
        contents = request.POST.get('contents')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("update liveblog_say set contents=%s,publicationdate=%s where id=%s",[contents,datetime.datetime.now(),id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('saying.html')

@login_required
def delsaying(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("delete from liveblog_say where id=%s",[nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('saying.html')

@login_required
def editmotus(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select id,theme,contents,successdate from liveblog_goals where id=%s",[nid])
        motus = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request,'writemotus.html',{'motus':motus})
    else:
        id = request.POST.get('id')
        title = request.POST.get('title')
        time = request.POST.get('time')
        content = request.POST.get('content')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("update liveblog_goals set theme=%s,contents=%s,successdate=%s where id=%s",[title,content,time,id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('motus.html')
@login_required
def delmotus(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("delete from liveblog_goals where id=%s",[nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('motus.html')


@csrf_exempt
@login_required()
def filesupload(request):
    file = request.FILES.get('file')
    filename = file.name.split('.')[0]
    file.name = 'liveblog-'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.'+file.name.split('.')[1]
    newfile = Files(
        name = filename,
        address = file,
        time = datetime.datetime.now()
    )
    newfile.save()
    path = "files/" + file.name
    res = {
        "code": 0
        ,"msg": "文件上传成功！!"
        ,'title':filename
        ,"data": {
        "src": path
  }
}
    return JsonResponse(res)