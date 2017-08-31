from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^test_tinymce/$', views.test_tinymce),  # 显示富文本
    url(r'^goods/(?P<goods_id>\d+)/$', views.goods_detail)  # 单个商品信息
]