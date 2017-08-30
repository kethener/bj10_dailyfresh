from django.conf.urls import url
from df_user import views


urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^check_user_name_exist/$', views.check_user_name_exist),
    url(r'^login/$', views.login),
    url(r'^login_check/$', views.login_check),
]
