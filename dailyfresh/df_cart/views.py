from django.shortcuts import render
from django.http import JsonResponse
from df_cart.models import Cart
from df_goods.models import Goods
from django.views.decorators.http import require_GET
from utils.decorators import login_required
# Create your views here.


@require_GET
@login_required
def cart_add(request):
    """添加商品到购物车"""
    # 1.获取商品的id和商品的数量
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    # 2.获取用户的id
    passport_id = request.session.get('passport_id')
    # 3.添加购物车记录
    # 3.1判断商品的库存是否小于goods_count
    # 先通过商品的id获取商品的信息
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods.goods_stock < int(goods_count):
        # 库存不足
        return JsonResponse({'res': 0})
    else:
        Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=int(goods_count))
        return JsonResponse({'res': 1})


@require_GET
@login_required
def cart_count(request):
    """获取购物车中商品的总数"""
    # 1.获取登陆用户id
    passport_id = request.session.get('passport_id')
    # 2.根据passport_id查询购物车中商品的总数
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    # 3.返回json数据
    return JsonResponse({'res': res})



