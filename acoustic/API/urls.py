from django.urls import path, re_path

from .views import GenerateReport, BaseAPIView, DownloadReport

urlpatterns = [
    path('', BaseAPIView.as_view()),
    re_path('^generate/?', GenerateReport.as_view()),
    re_path('^download/(?P<filename>(\w+-\d{2}-\d{2}_\d{4}\.\w+))', DownloadReport.as_view())
]
