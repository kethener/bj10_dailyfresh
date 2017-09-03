# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0002_auto_20170903_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='goodsa',
            new_name='goods',
        ),
    ]
