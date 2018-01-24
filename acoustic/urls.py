from django.urls import path, re_path, include

from django.contrib import admin
from acoustic.API.views import GenerateReport
admin.autodiscover()

urlpatterns = [
    re_path('^admin/?', admin.site.urls),
    path('api/', include('acoustic.API.urls'))
]
