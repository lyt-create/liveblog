# author:lytcreate
# blog:liveblog
# website:http://www.liveblog.cn
# powered by Django


from django.db import models
from django.contrib.auth.models import AbstractUser


class Myuser(AbstractUser):
    headimage = models.ImageField(upload_to='headimages',verbose_name='头像')
    birthday = models.DateField(auto_now=False,null=True,verbose_name='生日',blank=True)
    signs = models.CharField(max_length=60,null=True,verbose_name='个签')
    wechat = models.CharField(max_length=18,null=True,verbose_name='微信')
    weibo = models.CharField(max_length=18,null=True,verbose_name='微博')
    QQ = models.CharField(max_length=11,null=True,verbose_name='QQ')
    website = models.CharField(max_length=100,default='http://www.liveblog.cn',verbose_name='网站')
    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.QQ

class Say(models.Model):
    id = models.AutoField(primary_key=True)
    publisherid = models.CharField(max_length=7,null=True,verbose_name='作者ID')  # 发布人ID，获取头像，昵称
    contents = models.CharField(max_length=600,null=True,verbose_name='说说内容')  # 说说内容，不超过300字
    viewsnumber = models.IntegerField(default=0,verbose_name='浏览数')
    comments = models.IntegerField(default=0,verbose_name='评论')
    likesnumber = models.IntegerField(default=0,verbose_name='点赞数')
    publicationdate = models.DateTimeField(auto_now=False,verbose_name='发表时间')
    class Meta:
        verbose_name = '说说管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.contents

class Dailyrecord(models.Model):
    id = models.AutoField(primary_key=True)
    publisherid = models.IntegerField(default=0,verbose_name='作者ID')
    theme = models.CharField(max_length=60,null=True,verbose_name='日志主题')
    contents = models.TextField(max_length=4967295,null=True,verbose_name='日志内容')
    viewsnumber = models.IntegerField(default=0,verbose_name='浏览数')
    comments = models.IntegerField(default=0,verbose_name='评论数')
    likesnumber = models.IntegerField(default=0,verbose_name='点赞数')
    publicationdate = models.DateTimeField(auto_now=False,verbose_name='发表时间')
    image = models.ImageField(upload_to='images',verbose_name='日志封面图')
    class Meta:
        verbose_name = '日志管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.contents

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    articleid = models.IntegerField(default=0,null=True,verbose_name='文章ID')
    username = models.CharField(max_length=20,null=True,verbose_name='评论人')
    content = models.CharField(max_length=600,null=True,verbose_name='评论内容')
    publicationdate = models.DateTimeField(auto_now=False,verbose_name='评论时间')
    dadid = models.IntegerField(default=0,null=True,verbose_name='评论父ID')
    dadname = models.CharField(max_length=20,null=True,verbose_name='评论父姓名')
    email = models.CharField(max_length=30,null=True,verbose_name='评论人邮箱')
    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content

class Labels(models.Model):
    id = models.AutoField(primary_key=True)
    dailyid = models.CharField(max_length=7,null=True,verbose_name='日志ID')
    labelsname = models.CharField(max_length=20,null=True,verbose_name='标签名称')
    labelsnumber = models.IntegerField(default=0,verbose_name='标签数目')


class Goals(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=100,null=True,verbose_name='目标主题')
    contents = models.CharField(max_length=800,null=True,verbose_name='目标内容')
    state = models.CharField(max_length=50,null=True,verbose_name='目标状态')
    successdate = models.DateField(auto_now=False,verbose_name='未来之期')
    class Meta:
        verbose_name = '目标管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.contents

class Pictures(models.Model):
    id = models.AutoField(primary_key=True)
    publisherid = models.CharField(max_length=7,null=True,verbose_name='发布者ID')
    photos = models.ImageField(upload_to='pictures',verbose_name='照片')
    uploaddate = models.DateField(auto_now=False,verbose_name='发表日期')


class Links(models.Model):
    id = models.AutoField(primary_key=True)
    webname = models.CharField(max_length=20,null=True,verbose_name='网站名称')
    website = models.CharField(max_length=100,null=True,verbose_name='网站地址')
    class Meta:
        verbose_name = '友链管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.webname

class Photos(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='images',verbose_name='图片名称')
    time = models.DateTimeField(auto_now=False,verbose_name='上传时间')

class About(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=40,null=True,verbose_name='关于主题')
    content = models.TextField(max_length=4000,null=True,verbose_name='关于内容')
    time = models.DateTimeField(auto_now=False,verbose_name='关于时间')
    class Meta:
        verbose_name = '网站说明'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content

class Files(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True,verbose_name='名称')
    address = models.FileField(upload_to='files',verbose_name='附件地址')
    time = models.DateTimeField(auto_now=False,verbose_name='上传时间')