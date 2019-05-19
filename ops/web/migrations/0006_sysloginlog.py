# Generated by Django 2.2 on 2019-05-19 16:32

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_remove_loginlog_last_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysLoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loginname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '系统用户登陆日志',
                'db_table': 'sys_login',
                'ordering': ('create_time',),
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]