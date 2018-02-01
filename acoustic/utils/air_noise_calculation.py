from acoustic.utils.noise_calculation import NoiseCalculation

from acoustic.utils.functions import \
    transpose_matrix, get_exponents, get_fond_of_sound_absorption,\
    get_logarithm, get_frequency_response

EVALUATION_CURVE = [33,	36,	39,	42,	45,	48,	51,	52,	53,	54,	55,	56,	56,	56,	56,	56]


class AirNoiseCalculation(NoiseCalculation):
    air_noise_matrix = []
    transposed_air_noise_values = []
    average_air_noise_values = []

    def __init__(self, matrix, air_noise_matrix, reverberation_time, volume):
        self.air_noise_matrix = air_noise_matrix
        self.evaluation_curve = EVALUATION_CURVE
        super().__init__(matrix, reverberation_time, volume)

    def calculate_average_values(self):
        self.transposed_air_noise_values = transpose_matrix(self.air_noise_matrix)
        normalized_matrix = [get_exponents(x) for x in self.transposed_values]
        normalized_air_noise_matrix = [get_exponents(x) for x in self.transposed_air_noise_values]
        normalized_rt = get_fond_of_sound_absorption(self.reverberation_time, self.volume)
        reduced_values = [get_logarithm(x, self.calculations_quantity) for x in normalized_matrix]
        reduced_air_noise_values = [get_logarithm(x, self.calculations_quantity) for x in normalized_air_noise_matrix]
        self.average_values = list(reduced_values)
        self.average_air_noise_values = list(reduced_air_noise_values)
        values = [x - y for (x, y) in zip(reduced_air_noise_values, reduced_values)]
        return get_frequency_response(values, normalized_rt)