# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(verbose_name='用户名', max_length=20)),
                ('password', models.CharField(verbose_name='密码', max_length=40)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=254)),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
    ]
