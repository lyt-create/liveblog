# Generated by Django 3.1.2 on 2021-02-06 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveblog', '0006_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='website',
            field=models.CharField(max_length=100, null=True, verbose_name='网站'),
        ),
    ]
