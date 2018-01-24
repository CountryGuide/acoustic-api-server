from xlrd import open_workbook


def get_values_from_excel(file):
    frequencies = []

    wb = open_workbook(file_contents=file)
    for ws in wb.sheets():
        if ws.name != '1-1' and ws.name != '1-3':
            f = [ws.cell_value(x, 2) for x in range(67, 83)]
            frequencies.append(f)

    return frequencies
