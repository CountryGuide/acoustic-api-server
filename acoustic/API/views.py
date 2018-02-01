from distutils.util import strtobool

from django.http import HttpResponse, Http404
from django.views import View
from django.conf import settings
from os import path

from acoustic.utils.air_noise_calculation import AirNoiseCalculation
from acoustic.utils.extractor import get_values_from_excel
from acoustic.utils.noise_calculation import NoiseCalculation
from acoustic.utils.report_generator import generate_report


class BaseAPIView(View):
    def get(self):
        return HttpResponse('list of APIs')


class GenerateReport(View):
    def get(self):
        return HttpResponse('generate API')

    def post(self, request):
        reverberation_time = eval(request.POST['reverberation-time'], {'__builtins__': None}, {})
        volume = float(request.POST['volume'])
        air_mode = bool(strtobool(request.POST['air_mode']))
        file = request.FILES.get('data').read()
        data = get_values_from_excel(file)
        if air_mode:
            air_noise_source = request.FILES.get('air_noise').read()
            air_noise_data = get_values_from_excel(air_noise_source)
            results = AirNoiseCalculation(data, air_noise_data, reverberation_time, volume)
        else:
            results = NoiseCalculation(data, reverberation_time, volume)
        results.run_calculation()
        filename = generate_report(results.json)

        return HttpResponse(content=filename, content_type='application/json')


class DownloadReport(View):
    def get(self, **kwargs):
        file_path = path.join(settings.MEDIA_ROOT, kwargs['filename'])
        if path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + path.basename(file_path)
                return response
        raise Http404
