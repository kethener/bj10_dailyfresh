from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^test_tinymce/$', views.test_tinymce),  # 显示富文本
    url(r'^$', views.home_list_page),
    url(r'^goods/(?P<goods_id>\d+)/$', views.goods_detail),  # 显示单个商品详情
    url(r'^list/(\d+)/(\d+)/$', views.goods_list),  # 显示商品种类中的商品详情

    url(r'^get_image_list/$', views.get_image_list),
]