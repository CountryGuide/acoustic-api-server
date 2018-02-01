from acoustic.utils.noise_calculation import NoiseCalculation

EVALUATION_CURVE = [33,	36,	39,	42,	45,	48,	51,	52,	53,	54,	55,	56,	56,	56,	56,	56]


class AirNoiseCalculation(NoiseCalculation):
    air_noise_matrix = []

    def __init__(self, matrix, air_noise_matrix, reverberation_time, volume):
        self.air_noise_matrix = air_noise_matrix
        self.evaluation_curve = EVALUATION_CURVE
        super().__init__(matrix, reverberation_time, volume)
