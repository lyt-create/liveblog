# Generated by Django 3.1.2 on 2021-02-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveblog', '0007_myuser_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='website',
            field=models.CharField(default='http://www.liveblog.cn', max_length=100, verbose_name='网站'),
        ),
    ]