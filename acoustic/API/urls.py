from django.urls import path, re_path

from .views import GenerateReport, BaseAPIView

urlpatterns = [
    path('', BaseAPIView.as_view()),
    re_path('^generate/?', GenerateReport.as_view())
]