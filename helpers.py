class Helpers:
    def __init__(self):
        pass

    def map_range(x, in_min, in_max, out_min, out_max):
        val = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
        return min(max(val, out_min), out_max)