from acoustic.utils.noise_calculation import NoiseCalculation


class AirNoiseCalculation(NoiseCalculation):
    def __init__(self, matrix, reverberation_time, volume):
        super().__init__(matrix, reverberation_time, volume)
