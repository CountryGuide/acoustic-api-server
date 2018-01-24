from os import path
from datetime import datetime
from random import randint
from django.conf import settings

from openpyxl import Workbook
from openpyxl.styles import Alignment

from .main import FREQUENCIES, EVALUATION_CURVE as INITIAL_EVALUATION_CURVE


def generate_report(options):
    ac = Alignment(horizontal="center", vertical="center")

    wb = Workbook()
    ws_calc = wb.active
    ws_calc.title = 'Calculations'
    ws_rep = wb.create_sheet('Report')

    ws_rep['A1'] = 'Report generated at:'
    ws_rep['A2'] = datetime.now()

    ws_rep['A4'] = 'Показатель'
    ws_rep['A6'] = 'Средний уровень ударного шума под перекрытием, дБ'
    ws_rep['A7'] = 'Время реверберации,с'
    ws_rep['A8'] = 'Приведенный уровень шума, дБ'
    ws_rep['A9'] = 'Оценочная кривая'
    ws_rep['A10'] = 'Неблагоприятные отклонения'
    ws_rep['A11'] = 'Сумма неблагоприятных отклонений'
    ws_rep['A12'] = 'Целое число децибел, добавл./выч. из норм.кривой:'
    ws_rep['A14'] = 'Смещеная оценочная кривая, дБ'
    ws_rep['A15'] = 'Неблагоприятные отклонения'
    ws_rep['A16'] = 'Сумма неблагоприятных отклонений с учетом смещения оценочной кривой'
    ws_rep['A17'] = 'Индекс приведенного ударного шума'

    ws_rep['B4'] = 'Среднегеометрические частоты третьоктавных полос, Гц'

    ws_rep.merge_cells(start_row=4, start_column=1, end_row=5, end_column=1)
    ws_rep.merge_cells(start_row=4, start_column=2, end_row=4, end_column=17)

    for i in range(16):
        ws_rep.cell(row=5, column=(2 + i), value=FREQUENCIES[i])
        ws_rep.cell(row=6, column=(2 + i), value=options['logarithms'][i])
        ws_rep.cell(row=7, column=(2 + i), value=options['reverberation_times'][i])
        ws_rep.cell(row=8, column=(2 + i), value=options['frequency_response'][i])
        ws_rep.cell(row=9, column=(2 + i), value=INITIAL_EVALUATION_CURVE[i])
        ws_rep.cell(row=10, column=(2 + i), value=options['initial_deltas'][i])
        ws_rep.cell(row=14, column=(2 + i), value=options['results']['evaluation_curve'][i])
        ws_rep.cell(row=15, column=(2 + i), value=options['results']['deltas'][i])

    ws_rep['B11'] = options['initial_deltas_sum']
    ws_rep['B12'] = options['results']['evaluation_curve'][7] - INITIAL_EVALUATION_CURVE[7]
    ws_rep['B16'] = options['results']['deltas_sum']
    ws_rep['B17'] = options['results']['evaluation_curve'][7]

    now = str(datetime.date(datetime.now()))
    salt = str(randint(1000, 9999))
    file_name = 'Report_' + now + '_' + salt + '.xlsx'
    file_path = path.join(settings.MEDIA_ROOT, file_name)

    wb.save(file_path)

    return file_name
