from django.conf.urls import include, url
from django.contrib import admin
from eventualgram import views

urlpatterns = [
    url(r'', include('eventualgram.urls')),
    url(r'^admin/', admin.site.urls),
]
