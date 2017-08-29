from django.core.paginator import Paginator  # 导入分页类
from django.shortcuts import render
from df_goods.models import GoodsInfo, Goods
from df_goods.enums import *

# Create your views here.


def test_tinymce(request):
    """
    显示富文本
    """
    goods_info = GoodsInfo.objects.get(id=1)
    return render(request, 'test_tinymce.html', {'goods_info':goods_info})


def home_list_page(request):
    """显示首页内容"""
    # 1.查询每个种类商品的３个新品信息和４个商品信息
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)

    context = {'fruits_new': fruits_new, 'fruits': fruits}
    return render(request, 'index.html', context)


def goods_detail(request, goods_id):
    """显示商品详情页面"""
    # １.根据商品id查询商品信息
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 2.根据种类查询商品的新品信息
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 3.获取商品种类标题
    type_title = GOODS_TYPE[goods.goods_type_id]
    return render(request, 'detail.html', {'goods': goods,
                                           'goods_new_li': goods_new_li,
                                           'type_title': type_title})


def goods_list(request, goods_type_id, page_index):
    """显示商品列表页面"""
    # 获取排序方式
    sort = request.GET.get('sort', 'default')
    # 根据商品类型id获取商品信息
    goods_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, sort=sort)
    # 分页
    paginator = Paginator(goods_li, 1)
    # 获取页码列表
    pages = paginator.page_range
    # 取第page_index页的内容　有上一页:has_previous 有下一页:has_next 当前页:number
    goods_li = paginator.page(int(page_index))
    # 获取商品的新品信息
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, limit=2, sort='new')
    context = {'goods_li': goods_li, 'goods_new_li': goods_new_li,
               'type_id': goods_type_id, 'type_title': GOODS_TYPE[int(goods_type_id)],
               'pages': pages, 'sort': sort}
    return render(request, 'list.html', context)
