from django.http import HttpResponse
from django.views import View

from acoustic.utils.extractor import get_values_from_excel
from acoustic.utils.main import Calculation


class BaseAPIView(View):
    def get(self, request):
        return HttpResponse('list of APIs')


class GenerateReport(View):
    def get(self, request):
        return HttpResponse('generate API')

    def post(self, request):
        reverberation_time = eval(request.POST['reverberation-time'], {'__builtins__': None}, {})
        volume = float(request.POST['volume'])
        file = request.FILES.get('data').read()
        data = get_values_from_excel(file)
        results = Calculation(data, reverberation_time, volume)

        return HttpResponse(content=results.json, content_type='application/json')
