# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('recipient_name', models.CharField(max_length=20, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='收件地址')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮政编码')),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='所属账户')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
