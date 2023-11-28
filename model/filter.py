import numpy as np
from scipy import signal

class Filter:
    def __init__(self, object_vars_dict):
        self.cutoff = object_vars_dict["cutoff"]
        self.order = object_vars_dict["order"]
        self.gain = object_vars_dict["gain"]

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
    def __init__(self, object_vars_dict):
        super().__init__(object_vars_dict)

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
    def __init__(self, object_vars_dict):
        super().__init__(object_vars_dict)
        self.ripple = object_vars_dict["ripple"]

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


class FirWin(Filter):
    def __init__(self, object_vars_dict):
        super().__init__(object_vars_dict)
        self.numtaps = object_vars_dict["order"] + 1
        self.pass_zero = bool(object_vars_dict["pass_zero"])
        self.width = object_vars_dict["width"]
        self.window = object_vars_dict["window"]
        self.scale = bool(object_vars_dict["scale"])
        self.fs = object_vars_dict["fs"]
    def type(self):
        pass

    def filter_coefficients(self):
        """
        Compute coefficients of the filter
        :return: list
        """
        return signal.firwin(numtaps=self.numtaps,
                             cutoff=self.cutoff,
                             width=self.width,
                             window=self.window,
                             pass_zero=self.pass_zero,
                             scale=self.scale,
                             fs=self.fs)
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

    def freq_response(self):
        """
        Calculate frequency response of the filter in laplace space
        :param s: complex laplace space variable
        :return: complex filter response for s value
        """
        taps = self.filter_coefficients()
        w, h = signal.freqz(taps, worN=8000)
        return w, h

    def gain_phase_response(self, h):
        """
        Calculate gain and phase value of the frequency response
        :param h: The frequency response, as complex numbers
        :return: dict with gain and phase values
        """
        return {'Gain': np.abs(h),
                'Phase': np.unwrap(np.angle(h))}


def route_filter_class(object_vars_dict):
    """
    Create a filter of the selected class in the panel
    :param object_vars_dict: dictionary with the variables
    :return: object of the selected class
    """
    type_str = object_vars_dict["type_str"]
    if type_str == "Butterworth":
        filter_obj = Butterwoth(object_vars_dict)
    elif type_str == "Chebyshev":
        filter_obj = Chebyshev(object_vars_dict)
    elif type_str == "FIR_Window method (cutoff)":
        filter_obj = FirWin(object_vars_dict)
    return filter_obj
