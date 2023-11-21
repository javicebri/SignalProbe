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

    def phase_response(self, s):
        """
        Calculate phase values in radians of the frequency response for s
        tan−1[Im{X(ω)}Re{X(ω)}]
        :param s: np array of complex laplace space variables
        :return: np array of values
        """
        return np.unwrap(np.angle(self.freq_response(s)))

    def gain_response(self, s):
        """
        Calculate gain values of the frequency response for s
        :param s: np array of complex laplace space variables
        :return: np array of values
        """
        return np.abs(self.freq_response(s))

    def gain_phase_response(self, s):
        """
        Calculate gain and phase value of the frequency response for s
        :param s: np array of complex laplace space variables
        :return: dict with gain and phase values
        """
        fr = self.freq_response(s)
        return {'Gain': np.abs(fr),
                'Phase': np.unwrap(np.angle(fr))}

class Butterwoth(Filter):
    def __init__(self, cutoff, order, gain=1):
        super().__init__(cutoff, order, gain)

    def type(self):
        pass

    def freq_response(self, s):
        """
        Calculate frequency response of the filter in laplace space
        :param s: complex laplace space variable
        :return: complex filter response for s value
        """

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


class Chebyshev(Filter):
    def __init__(self, cutoff, order, gain=1, ripple=1):
        super().__init__(cutoff, order, gain)
        self.ripple = ripple
    def type(self):
        pass

    def pole_i(self, i, eps, n):
        """
        si pole value
        :param i: int number of the pole
        :param eps: float epsilon = srqt(10**r/10 - 1) with r the ripple in dB
        :param n: int order of the filter
        :return: complex si
        """
        gamma = ((1 + np.sqrt(1 + eps**2)) / eps)**(1/n)
        sig = (((1/gamma)-gamma)/2) * np.sin(((2*i - 1)*np.pi) / (2*n))
        omg = (((1/gamma)+gamma)/2) * np.cos(((2*i - 1)*np.pi) / (2*n))
        return complex(sig, omg)

    def freq_response(self, s):
        """
        Calculate frequency response of the filter in laplace space
        :param s: complex laplace space variable
        :return: complex filter response for s value
        """

        n = int(self.order)
        r = self.ripple
        eps = np.sqrt(10**(r/10) - 1)

        G_0 = self.gain
        A_n = 1  # Numer
        B_n = 1

        for i in range(1, n + 1):
            A_n = A_n * (- self.pole_i(i, eps, n))
            B_n = B_n * (s - self.pole_i(i, eps, n))

        if n % 2 == 0:
            #Even
            A_n = A_n * 10**(r/20)

        return G_0 * (A_n/B_n)


def route_filter_class(type_str, cutoff, order, gain=1, ripple=1):
    """
    Create a filter of the selected class in the panel
    :param type_str: str with filter type
    :param cutoff: float with cutoff frequency
    :param order: int with the filter order
    :param gain: float with filter gain value
    :param ripple: float ripple in dB
    :return: object of the selected class
    """
    if type_str == "Butterworth":
        filter_obj = Butterwoth(cutoff, order, gain)
    elif type_str == "Chebyshev":
        filter_obj = Chebyshev(cutoff, order, gain, ripple)
    return filter_obj