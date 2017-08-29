# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('img_url', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('is_def', models.BooleanField(verbose_name='是否默认', default=False)),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
