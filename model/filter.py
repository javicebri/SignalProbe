import math
from abc import ABC, abstractmethod

import numpy as np
from scipy import signal


class FResponse(ABC):
    @abstractmethod
    def calc_f_response(self):
        pass


class ZeroPole(ABC):
    @abstractmethod
    def calc_zero_pole(self):
        pass


class FilterCoefficients(ABC):
    @abstractmethod
    def calc_filter_coefficients(self):
        pass


class Filter(FResponse, ZeroPole, ABC):
    def __init__(self, h, f_axis, gain_values, phase_values, zeros, poles, sys_gain):
        self._h = h
        self._f_axis = f_axis
        self._gain_values = gain_values
        self._phase_values = phase_values
        self._zeros = zeros
        self._poles = poles
        self._sys_gain = sys_gain

    @abstractmethod
    def calc_f_response(self):
        pass

    @property
    def f_axis(self):
        return self._f_axis

    @property
    def gain_values(self):
        return self._gain_values

    @property
    def phase_values(self):
        return self._phase_values

    @property
    def zeros(self):
        return self._zeros

    @property
    def poles(self):
        return self._poles

    @property
    def gain_values(self):
        return self._gain_values

    @property
    def phase_values(self):
        return self._phase_values

    def calc_gain(self):
        self._gain_values = np.abs(self._h)

    def calc_phase(self):
        self._phase_values = np.unwrap(np.angle(self._h))


class DFilter(Filter, FilterCoefficients, ABC):
    def __init__(self, fs, taps, h, f_axis, gain_values, phase_values, zeros, poles, sys_gain):
        super().__init__(h, f_axis, gain_values, phase_values, zeros, poles, sys_gain)
        self._fs = fs
        self._taps = taps

    @property
    def fs(self):
        return self._fs

class FirWin(DFilter):
    def __init__(self, order, cutoff, pass_zero,
                 width, window, scale,
                 fs, taps=None, h=None,
                 f_axis=None, gain_values=None, phase_values=None,
                 zeros=None, poles=None, sys_gain=None):

        super().__init__(fs, taps, h, f_axis, gain_values, phase_values, zeros, poles, sys_gain)
        self._order = order
        self._numtaps = order + 1
        self._cutoff = cutoff
        self._pass_zero = pass_zero
        self._width = width
        self._window = window
        self._scale = scale

        self.calc_filter_coefficients()
        self.calc_f_response()
        self.calc_gain()
        self.calc_phase()
        self.calc_zero_pole()

    def calc_filter_coefficients(self):
        self._taps = signal.firwin(numtaps=self._numtaps,
                                   cutoff=self._cutoff,
                                   width=self._width,
                                   window=self._window,
                                   pass_zero=self._pass_zero,
                                   scale=self._scale,
                                   fs=self._fs)

    def calc_f_response(self):
        w, self._h = signal.freqz(self._taps, worN=512)
        self._f_axis = (w / (2 * np.pi)) * self._fs

    def calc_zero_pole(self):
        self._zeros, self._poles, self._sys_gain = signal.tf2zpk(self._taps, 1)


class AFilter(Filter, ABC):
    def __init__(self, cutoff):
        self._s = None
        self._cutoff = cutoff

    def calc_s_vector(self):
        freq_units = math.floor(math.log(self._cutoff, 10))
        n_points = max(int(100 * freq_units), 1000)  # Ensure a min of points
        n_points = min(n_points, int(100 * 1e3))
        end_point = complex(0, self._cutoff * freq_units * 10)
        init_point = complex(0, 0.10)
        self._s = np.geomspace(init_point, end_point, n_points)


class Butterwoth(AFilter):
    def __init__(self, order, target_gain):
        self._order = order
        self._target_gain = target_gain

        self.calc_s_vector()
        self.calc_gain()
        self.calc_phase()

    def calc_f_response(self):
        n = self._order
        g_0 = self._target_gain
        b_n = 1
        if n % 2 == 0:
            # Even
            for k in range(1, int(n / 2) + 1):
                b_n = b_n * (self._s ** 2 - 2 * self._s * np.cos((2 * k + n - 1) / (2 * n) * np.pi) + 1)
        else:
            for k in range(1, int((n - 1) / 2) + 1):
                b_n = b_n * (self._s ** 2 - 2 * self._s * np.cos((2 * k + n - 1) / (2 * n) * np.pi) + 1)
            b_n = b_n * (self._s + 1)

        self._f_axis = self._s.imag
        self._gain_values = g_0 / b_n

    def calc_zero_pole(self):
        pass



class Chebyshev(AFilter):
    def __init__(self, order, target_gain, ripple):
        self._order = order
        self._target_gain = target_gain
        self._ripple = ripple

        self.calc_s_vector()
        self.calc_gain()
        self.calc_phase()

    def pole_i(self, i, eps, n):
        """
        si pole value
        :param i: int number of the pole
        :param eps: float epsilon = srqt(10**r/10 - 1) with r the ripple in dB
        :param n: int order of the filter
        :return: complex si
        """
        gamma = ((1 + np.sqrt(1 + eps ** 2)) / eps) ** (1 / n)
        sig = (((1 / gamma) - gamma) / 2) * np.sin(((2 * i - 1) * np.pi) / (2 * n))
        omg = (((1 / gamma) + gamma) / 2) * np.cos(((2 * i - 1) * np.pi) / (2 * n))
        return complex(sig, omg)

    def calc_f_response(self):
        n = self._order
        g_0 = self._target_gain
        r = self.ripple
        eps = np.sqrt(10 ** (r / 10) - 1)

        a_n = 1  # Numer
        b_n = 1

        for i in range(1, n + 1):
            a_n = a_n * (- self.pole_i(i, eps, n))
            b_n = b_n * (self._s - self.pole_i(i, eps, n))

        if n % 2 == 0:
            # Even
            a_n = a_n * 10 ** (r / 20)

        return g_0 * (a_n / b_n)

    def calc_zero_pole(self):
        pass


def route_filter_class(object_vars_dict):
    """
    Create a filter of the selected class in the panel
    :param object_vars_dict: dictionary with the variables
    :return: object of the selected class
    """
    type_str = object_vars_dict["type_str"]

    if type_str == "Butterworth":
        filter_obj = Butterwoth(**object_vars_dict)
    elif type_str == "Chebyshev":
        filter_obj = Chebyshev(**object_vars_dict)
    elif type_str == "FIR_Window method (cutoff)":
        arg_keys = ['order', 'cutoff', 'width', 'window', 'pass_zero', 'scale', 'fs']
        filtered_dict = {k: object_vars_dict[k] for k in arg_keys}
        filter_obj = FirWin(**filtered_dict)
    return filter_obj
