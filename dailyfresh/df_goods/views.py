from django.shortcuts import render

from df_goods.enums import *
from df_goods.models import GoodsInfo, Goods


# Create your views here.


def test_tinymce(request):
    """显示富文本"""
    goods_info = GoodsInfo.objects.get(id=1)
    return render(request, 'test_tinymce.html', {'goods_info': goods_info})


def goods_detail(request, goods_id):
    """商品详情页"""
    # 1. 根据商品id获取商品信息
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 2. 根据种类查询商品的信息
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 3. 获取商品种类标题
    type_title = GOODS_TYPE[goods.goods_type_id]
    return render(request, 'detail.html', {'goods': goods,
                                           'goods_new_li': goods_new_li,
                                           'type_title': type_title})
