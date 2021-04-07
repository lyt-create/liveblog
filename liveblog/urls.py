"""liveblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# author:lytcreate
# blog:liveblog
# website:http://www.liveblog.cn
# powered by Django



from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.static import serve

from liveblog import views
from liveblog.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login.html', views.login),
    path('', views.home),
    path('home.html', views.home),
    path('saying.html',views.saying),
    path('album.html',views.album),
    path('motus.html',views.motus),
    path('timeline.html',views.timeline),
    path('about.html',views.about),
    path('logout.html',views.logout),
    path('albums.html',views.albums),
    path('publish.html',views.publish),
    path('upload/',views.upload),       #富文本编辑器上传图片返回json
    path('daily.html',views.daily),
    path('publishcomments.html',views.publishcomments),
    path('updatesaylike/',views.updatesaylike),
    path('dailylikes/',views.dailylikes),
    path('updateabout.html',views.updateabout),
    path('writemotus.html',views.writemotus),
    path('motussuccess.html',views.motussuccess),
    path('editdaily.html',views.editdaily),
    path('editlinks.html',views.editlinks),
    path('deldaily.html',views.deldaily),
    path('deldaily.html',views.deldaily),
    path('editsaying.html',views.editsaying),
    path('delsaying.html',views.delsaying),
    path('editmotus.html',views.editmotus),
    path('delmotus.html',views.delmotus),
    path('timelines.html',views.timelines),
    path('filesupload/',views.filesupload),

    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    # url(r'^upload/$', views.upload, name='detail'),

]
