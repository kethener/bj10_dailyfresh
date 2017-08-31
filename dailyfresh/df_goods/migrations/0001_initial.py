# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_type_id', models.SmallIntegerField(verbose_name='商品种类id', choices=[(1, '新鲜水果'), (2, '海鲜水果'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')])),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_sub_title', models.CharField(max_length=256, verbose_name='商品副标题')),
                ('goods_price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='商品运费', decimal_places=2, max_digits=10)),
                ('goods_unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('goods_stock', models.IntegerField(verbose_name='商品库存', default=0)),
                ('goods_sales', models.IntegerField(verbose_name='商品销量', default=0)),
                ('goods_status', models.SmallIntegerField(verbose_name='商品库存', default=1)),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品详情')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('img_url', models.ImageField(verbose_name='商品图片', upload_to='goods')),
                ('id_def', models.BooleanField(verbose_name='是否默认', default=False)),
                ('goods', models.ForeignKey(verbose_name='所属商品', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
