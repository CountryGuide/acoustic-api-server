from xlrd import open_workbook


def get_values_from_excel(file):
    frequencies = []

    wb = open_workbook(file_contents=file)
    for ws in wb.sheets():
        if ws.name != '1-1' and ws.name != '1-3':
            f = []
            for i in range(67, 83):
                f.append(ws.cell_value(i, 2))
            frequencies.append(f)
    # j = 0
    # for ws in wb.sheets():
    #     for i in range(67, 83):
    #         frequencies[j].append(ws.cell_value(i, 2))
    #     j += 1

    return frequencies
