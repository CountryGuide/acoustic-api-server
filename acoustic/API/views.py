from django.http import HttpResponse
from django.views import View

# Create your views here.


class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('test')
