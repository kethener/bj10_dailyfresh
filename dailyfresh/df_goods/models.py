from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class GoodsInfo(models.Model):
    '''
    商品信息类
    '''
    goods_info = HTMLField(verbose_name='商品详情')