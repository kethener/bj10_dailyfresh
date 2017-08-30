from django.shortcuts import render
from df_goods.models import GoodsInfo
# Create your views here.

def test_tinymce(request):
    '''
    显示富文本
    '''
    goods_info = GoodsInfo.objects.get(id=1)
    return render(request, 'test_tinymce.html', {'goods_info':goods_info})

