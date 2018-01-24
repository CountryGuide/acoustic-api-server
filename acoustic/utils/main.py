import json

from .functions import *

# оценочная кривая
EVALUATION_CURVE = [62, 62, 62, 62, 62, 62, 61, 60, 59, 58, 57, 54, 51, 48, 45, 42]

# какой-то параметр калибровочный, не знаю как называется
CORRECTION_PARAMETER = -32

# Частоты, Гц
FREQUENCIES = [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150]


class Calculation:
    frequencies = FREQUENCIES
    values = []
    transposed_values = []
    average_values = []
    deltas = []
    evaluation_curve = []
    reverberation_time = []
    volume = 0
    calculations_quantity = 0

    def __init__(self, matrix, reverberation_time, volume):
        print('Created new calculation')
        self.values = matrix
        self.reverberation_time = reverberation_time
        self.evaluation_curve = EVALUATION_CURVE
        self.volume = volume
        self.calculations_quantity = len(self.values)
        self.run_calculation()

    def run_calculation(self):
        self.transposed_values = transpose_matrix(self.values)
        self.average_values = [round(x) for x in self.calculate_average_values()]
        self.log()
        if self.calculate_deltas(self.evaluation_curve) == CORRECTION_PARAMETER:
            pass
        elif self.calculate_deltas(self.evaluation_curve) > CORRECTION_PARAMETER:
            self.decrease_evaluation_curve()
        else:
            self.increase_evaluation_curve()
        self.log()

    def calculate_average_values(self):
        normalized_matrix = [get_exponents(x) for x in self.transposed_values]
        normalized_rt = get_fond_of_sound_absorption(self.reverberation_time, self.volume)
        reduced_values = [get_logarithm(x, self.calculations_quantity) for x in normalized_matrix]
        return get_frequency_response(reduced_values, normalized_rt)

    def calculate_deltas(self, curve):
        self.deltas = filter_negative_results(get_deltas(curve, self.average_values))
        return sum([round(x) for x in self.deltas])

    def increase_evaluation_curve(self):
        curve = self.evaluation_curve[:]
        while self.calculate_deltas(curve) <= CORRECTION_PARAMETER:
            if self.calculate_deltas(curve) <= CORRECTION_PARAMETER:
                curve = [x + 1 for x in curve]
                self.evaluation_curve = curve

    def decrease_evaluation_curve(self):
        curve = list(self.evaluation_curve)
        while self.calculate_deltas(curve) >= CORRECTION_PARAMETER:
            self.evaluation_curve = curve
            if self.calculate_deltas(curve) >= CORRECTION_PARAMETER:
                curve = [x - 1 for x in curve]

    def log(self):
        print('{0}\n{1}\n{2}\n{3}'.format(
            self.calculate_deltas(self.evaluation_curve),
            self.evaluation_curve,
            self.average_values,
            self.deltas
        ))

    @property
    def json(self):
        result = {
            'deltas': self.calculate_deltas(self.evaluation_curve),
            'evc': self.evaluation_curve,
            'average values': self.average_values
        }
        return json.dumps(result)
