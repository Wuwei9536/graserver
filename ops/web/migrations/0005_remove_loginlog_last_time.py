# Generated by Django 2.2 on 2019-05-16 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20190511_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginlog',
            name='last_time',
        ),
    ]