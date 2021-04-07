# Generated by Django 3.1.2 on 2021-02-04 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='content',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='dailyrecord',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
