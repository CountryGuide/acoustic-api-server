from django.urls import path, re_path
from django.conf.urls import url

from django.contrib import admin
from acoustic.API.views import TestView
admin.autodiscover()

urlpatterns = [
    re_path('^admin/?', admin.site.urls),
    re_path('^api/?', TestView.as_view())
]
