from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add),  # 添加商品到购物车
    url(r'^count/$', views.cart_count),  # 统计购物车中商品的数目
    url(r'^update/$', views.cart_update),  # 更新购物车商品的数目
    url(r'^$', views.cart_show),
]
