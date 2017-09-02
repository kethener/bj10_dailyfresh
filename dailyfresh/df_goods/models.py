from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
from df_goods.enums import *
from db.base_manager import BaseManager
# Create your models here.


class GoodsInfo(models.Model):
    """
    商品信息类
    """
    goods_info = HTMLField(verbose_name='商品详情')


class GoodsLoginManager(BaseManager):
    """商品逻辑模型管理器类"""
    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        """根据商品种类id获取商品信息"""
        goods_list = Goods.objects.get_goods_list_by_type(goods_type_id=goods_type_id,
                                                          limit=limit, sort=sort)
        for goods in goods_list:
            # 根据商品的id查询商品图片
            img = Image.objects.get_image_by_goods_id(goods_id=goods.id)
            # 给goods对象增加一个img_url属性，用于记住商品图片的路径
            goods.img_url = img.img_url  # ''当图片不存在的时候，代码不会出错，而是会赋值为空字符串
        return goods_list

    def get_goods_by_id(self, goods_id):
        """根据商品的id获取商品信息"""
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        img = Image.objects.get_image_by_goods_id(goods_id=goods.id)
        # 给goods对象增加一个img_url属性，用于记住商品的图片路径
        goods.img_url = img.img_url
        return goods


class GoodsManager(BaseManager):
    """商品模型管理器类"""
    def get_goods_by_id(self, goods_id):
        """根据商品的ｉｄ获取商品信息"""
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        """根据商品种类的id获取商品的信息"""
        if sort == 'new':
            # 按照新品进行排序
            # 减号为从高到低，不加为从低到高
            order_by = ('-create_time',)
        elif sort == 'price':
            # 按照价格查询商品
            order_by = ('goods_price',)
        elif sort == 'hot':
            # 按照热度查询商品
            order_by = ('-goods_sales',)
        else:
            # 按照默认方式查询商品
            order_by = ('-pk',)
        goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=order_by)
        if limit:
            goods_list = goods_list[:limit]
        return goods_list


class Goods(BaseModel):
    """商品模型类"""
    goods_type_choice = (
        (FRUIT, GOODS_TYPE[FRUIT]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    )

    # 1-6之间,下拉列表框
    goods_type_id = models.SmallIntegerField(choices=goods_type_choice,
                                             verbose_name='商品种类id')
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=256, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      verbose_name='商品价格')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name='商品运费')
    goods_unite = models.CharField(max_length=20, verbose_name='商品单位')
    goods_info = HTMLField(verbose_name='商品详情')
    goods_stock = models.IntegerField(default=0, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    # ０代表下线商品，　１代表上线商品
    goods_status = models.SmallIntegerField(default=1, verbose_name='商品状态')

    objects = GoodsManager()
    objects_logic = GoodsLoginManager()

    class Meta:
        db_table = 's_goods'


class ImageManager(BaseManager):
    """商品图片模型管理器类"""
    def get_image_by_goods_id(self, goods_id):
        images = self.get_object_list(filters={'goods_id': goods_id})
        if images.exists():
            # 说明商品有图片
            images = images[0]  # Image类型的对象
        else:
            # 说明商品没有图片
            images.img_url = ''
        return images

    def get_images_by_goods_id_list(self, goods_id_list):  # __in
        '''
        根据goods_id_list获取图片的查询集
        '''
        image_list = self.get_object_list(filters={'goods_id__in': goods_id_list})
        return image_list


class Image(BaseModel):
    """商品图片模型类"""
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods', verbose_name='商品图片')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = ImageManager()

    class Meta:
        db_table = 's_goods_image'
