from django.http import HttpResponse
from django.views import View

from acoustic.utils.extractor import get_values_from_excel
from acoustic.utils.main import Calculation

# Create your views here.
REVERBERATION_TIMES = [0.617, 0.592, 0.454, 0.367, 0.370, 0.399, 0.436, 0.423,
                       0.374, 0.386, 0.364, 0.342, 0.366, 0.385, 0.381, 0.442]


class BaseAPIView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('list of APIs')


class GenerateReport(View):
    def get(self, request):
        return HttpResponse('generate API')

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('data').read()
        data = get_values_from_excel(file)
        results = Calculation(data, REVERBERATION_TIMES, 32)

        return HttpResponse(content=results.json, content_type='application/json')
