from django.db import models
from django.db.models import Sum  # 导入聚合函数
from db.base_manager import BaseManager
from db.base_model import BaseModel
# Create your models here.


class CartManager(BaseManager):
    """
    定义模型管理器类
    """
    def get_one_cart_info(self, passport_id, goods_id):
        """获取用户购物车中的某条信息"""
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self,passport_id, goods_id, goods_count):
        """添加购物车记录"""
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        # 判断用户的购物车中是否已经添加过该商品
        if cart_info is None:
            # 购物车中没有添加过该商品，新创建一个该商品记录
            cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        else:
            # 购物车中有该商品，在原商品数量上加上加入购物车商品的数量就可以了
            cart_info.goods_count = cart_info.goods_count + goods_count
            cart_info.save()
        # 返回结果
        return cart_info

    def get_cart_count_by_passport(self, passport_id):
        """根据passport_id获取购物车中的商品的总数"""
        # 根据账户获取商品的查询集，再进行聚合函数操作，返回字典，结果为{'goods_count__sum':结果}
        res_dict = self.get_object_list(filters={'passport_id': passport_id}).aggregate(Sum('goods_count'))
        # 对字典进行取值，
        res = res_dict['goods_count__sum']
        # 判断结果，如果没有查询到商品信息会显示None，此时需要将结果返回0，
        if res is None:
            res = 0
        return res


class Cart(BaseModel):
    """定义购物车模型类"""
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='所属商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数量')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'
