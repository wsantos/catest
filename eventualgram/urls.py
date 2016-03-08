from django.conf.urls import url
from eventualgram import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
