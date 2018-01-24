import math


def get_fond_of_sound_absorption(lst: list, vol: float) -> list:
    """
    Формула для расчета фонда звукопоглощения
    """
    return [round(0.16 * vol / x, 3) for x in lst]


def transpose_matrix(mtx: list) -> list:
    """
    Функция для транспонирования матриц
    """
    return list(map(list, zip(*mtx)))


def get_exponents(lst: list) -> list:
    """
    Функция расчета каких-то экспонент
    """
    return [10 ** (0.1 * x) for x in lst]


def get_logarithm(lst: list, quantity_of_msr: int) -> float:
    """
    Функция расчета каких-то десятичных логарифмов
    """
    return 10 * math.log10(1 / quantity_of_msr * sum(lst))


def get_frequency_response(logarithms: list, fosa: list) -> list:
    """
    Функция расчета значений частотной характеристики
    """
    return list(map(lambda x, y: x + 10 * math.log10(y / 10), logarithms, fosa))


def get_deltas(results: list, ev_curve: list) -> list:
    """
    Функция расчета дельт соответствующих значений частотной характеристики и оценочной кривой
    """
    return list(map(lambda x, y: x - y, results, ev_curve))


def filter_positive_results(lst: list) -> list:
    """
    Функция-фильтр, отсекает отрицательные и нулевые значения
    """
    return list(filter(lambda x: x > 0, lst))


def filter_negative_results(lst: list) -> list:
    """
    Функция-фильтр, отсекает положительные и нулевые значения
    """
    return list(filter(lambda x: x < 0, lst))


def decrease_evaluation_curve(ev_curve: list) -> list:
    """
    Функция корректировки оченочной кривой вниз
    """
    return [x - 1 for x in ev_curve]
