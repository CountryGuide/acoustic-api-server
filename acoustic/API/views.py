import json

from django.http import HttpResponse
from django.views import View

from acoustic.utils.extractor import get_values_from_excel
# Create your views here.


class BaseAPIView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('list of APIs')


class GenerateReport(View):
    def get(self, request):
        return HttpResponse('generate API')

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('data').read()
        data = json.dumps(get_values_from_excel(file))

        return HttpResponse(content=data, content_type='application/json')
