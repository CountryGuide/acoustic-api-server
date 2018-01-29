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
    reverberation_time = []
    transposed_values = []
    evaluation_curve = []
    average_values = []
    reduced_values = []
    values = []
    deltas = []
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
        self.reduced_values = [round(x) for x in self.calculate_average_values()]
        if sum(self.calculate_deltas(self.evaluation_curve)) == CORRECTION_PARAMETER:
            pass
        elif sum(self.calculate_deltas(self.evaluation_curve)) < CORRECTION_PARAMETER:
            self.decrease_evaluation_curve()
        else:
            self.increase_evaluation_curve()

    def calculate_average_values(self):
        normalized_matrix = [get_exponents(x) for x in self.transposed_values]
        normalized_rt = get_fond_of_sound_absorption(self.reverberation_time, self.volume)
        reduced_values = [get_logarithm(x, self.calculations_quantity) for x in normalized_matrix]
        self.average_values = list(reduced_values)
        return get_frequency_response(reduced_values, normalized_rt)

    def calculate_deltas(self, curve):
        self.deltas = filter_negative_results(get_deltas(self.reduced_values, curve))
        return [round(x) for x in self.deltas]

    def calculate_deltas_for_report(self, curve):
        self.deltas = get_deltas(self.reduced_values, curve)
        return [round(x) if x < 0 else '' for x in self.deltas]

    def increase_evaluation_curve(self):
        curve = self.evaluation_curve[:]
        while sum(self.calculate_deltas(curve)) >= CORRECTION_PARAMETER:
            self.evaluation_curve = curve
            if sum(self.calculate_deltas(curve)) >= CORRECTION_PARAMETER:
                curve = [x + 1 for x in curve]

    def decrease_evaluation_curve(self):
        curve = list(self.evaluation_curve)
        while sum(self.calculate_deltas(curve)) <= CORRECTION_PARAMETER:
            if sum(self.calculate_deltas(curve)) <= CORRECTION_PARAMETER:
                curve = [x - 1 for x in curve]
                self.evaluation_curve = curve

    def log(self):
        print('{0}\n{1}\n{2}\n{3}'.format(
            sum(self.calculate_deltas(self.evaluation_curve)),
            self.evaluation_curve,
            self.reduced_values,
            self.deltas
        ))

    @property
    def json(self):
        result = {
            'average': [round(x) for x in self.average_values],
            'reverberation-time': [round(x, 2) for x in self.reverberation_time],
            'reduced': self.reduced_values,
            'evaluation_curve': EVALUATION_CURVE,
            'initial_deltas': self.calculate_deltas_for_report(EVALUATION_CURVE),
            'initial_deltas_sum': sum(self.calculate_deltas(EVALUATION_CURVE)),
            'dB_difference': self.evaluation_curve[0] - EVALUATION_CURVE[0],
            'reduced_evaluation_curve': self.evaluation_curve,
            'deltas': self.calculate_deltas_for_report(self.evaluation_curve),
            'deltas_sum': sum(self.calculate_deltas(self.evaluation_curve)),
            'reduced_noise_index': self.evaluation_curve[7]
        }
        return json.dumps(result)
