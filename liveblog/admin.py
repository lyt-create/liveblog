# author:lytcreate
# blog:liveblog
# website:http://www.liveblog.cn
# powered by Django

from django.contrib import admin

from .models import Myuser, Say, Dailyrecord, Comments, Goals, Links, About
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
@admin.register(Myuser)
class MyUserAdmin(UserAdmin):
    list_display = ['username','signs','email','birthday','headimage']
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (_('Personal info'),
                    {'fields':('signs','email','birthday','headimage','weibo','wechat','QQ','website')})

class SayAdmin(admin.ModelAdmin):
    list_display = ['contents','publicationdate']
    list_filter = ['publicationdate']
    search_fields = ['publicationdate','contents']
admin.site.register(Say,SayAdmin)

class DailyrecordAdmin(admin.ModelAdmin):
    list_display = ['theme','viewsnumber','comments','likesnumber','publicationdate']
    list_filter = ['theme','publicationdate']
    search_fields = ['theme','contents']
admin.site.register(Dailyrecord,DailyrecordAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['articleid','username','content','publicationdate']
    list_filter = ['username','publicationdate']
    search_fields = ['articleid','username','content','dadname']
admin.site.register(Comments,CommentsAdmin)

class GoalsAdmin(admin.ModelAdmin):
    list_display = ['theme','state','successdate']
    list_filter = ['theme','state','successdate']
    search_fields = ['theme','contents','state']
admin.site.register(Goals,GoalsAdmin)

class LinksAdmin(admin.ModelAdmin):
    list_display = ['webname','website']
admin.site.register(Links,LinksAdmin)

class AboutAdmin(admin.ModelAdmin):
    list_display = ['subject','time']
admin.site.register(About,AboutAdmin)