from django.conf.urls import url
from df_user import views


urlpatterns = [
    url(r'^index$', views.index)
]