from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^test_tinymce/$', views.test_tinymce),  # 显示富文本
]