# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_image'),
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_count', models.IntegerField(verbose_name='商品数量', default=1)),
                ('goods', models.ForeignKey(verbose_name='所属商品', to='df_goods.Goods')),
                ('passport', models.ForeignKey(verbose_name='账户', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
