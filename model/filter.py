import numpy as np

class Filter:
    def __init__(self, cutoff, order, gain=1):
        self.cutoff = cutoff
        self.order = order
        self.gain = gain

    def type(self):
        pass

    def freq_response(self):
        pass

    def phase_response(self):
        pass

    def gain_response(self, s):
        return np.abs(self.freq_response(s))

class Butterwoth(Filter):
    def __init__(self, cutoff, order, gain=1):
        super().__init__(cutoff, order, gain)

    def type(self):
        pass

    def freq_response(self, s):

        n = int(self.order)
        G_0 = self.gain
        B_n = 1
        if n % 2 == 0:
            #Even
            for k in range(1, int(n/2) + 1):
                B_n = B_n * (s**2 - 2*s * np.cos((2*k + n - 1)/(2*n) * np.pi) + 1)
        else:
            for k in range(1, int((n-1)/2) + 1):
                B_n = B_n * (s**2 - 2*s * np.cos((2*k + n - 1)/(2*n) * np.pi) + 1)
            B_n = B_n * (s + 1)

        return G_0/B_n

    def phase_response(self):
        pass

def route_filter_class(type_str, cutoff, order, gain=1):
    if type_str == "Butterworth":
        filter_obj = Butterwoth(cutoff, order, gain)
    return filter_obj

def butterworth_filter_calculator(cutoff_freq, freq_units):
    pass