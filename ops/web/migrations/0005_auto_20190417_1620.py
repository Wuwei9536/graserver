# Generated by Django 2.2 on 2019-04-17 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20190417_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersystem',
            name='groupname',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='usersystem',
            name='homedirectory',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
