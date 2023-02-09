import numpy as np

class NullStreamBaseTD:
    """ Time-domain null stream time series object. Calling an instance 
    of this object provides network null stream time series data. 
    Time-domain null stream, strain response at time delay difference 
    is obtained through interpolation.

    Parameters
    ==========
    projected_strain_dict: dict
        A dict of `numpy.ndarray`, with keys corresponding to detector 
        indices. The reference detector index, with respect to which
        null stream is calculated, must be 0.
    time_array_dict: dict
        A dict of `numpy.ndarray` with times corresponding to
        projected strain time series.
    time_delay_dict: dict
        A dict of time delays with respect to detector 0.
    f_plus_dict: dict
        A dict with F_+ corresponding to detectors.
    f_cross_dict: dict
        A dict with F_x corresponding to detectors.

    Returns
    =======
    network_null_stream: `numpy.ndarray`
        Sky position dependent network null stream
    et_null_stream: `numpy.ndarray`
        ET null stream independent of gravitational wave source
        parameters
    """
    def __init__(self, projected_strain_dict, time_array_dict, 
                 time_delay_dict, f_plus_dict, f_cross_dict):
        self.proj_strain = projected_strain_dict
        self.time_array = time_array_dict
        self.time_delay = time_delay_dict
        self.f_p = f_plus_dict
        self.f_x = f_cross_dict
        self.add_readable_antenna_pattern_variables()

        self.nn = len(self.proj_strain[0])

        self._network_null_stream = None
        self._et_null_stream = None
        self._corrected_strain = None
        self._strain_interpolants = None

    def update_network_null_stream(self):
        self._network_null_stream = np.zeros(self.nn)
        for cs in self.corrected_strain.values():
            self._network_null_stream += cs

    def update_et_null_stream(self):
        self._et_null_stream = np.zeros(self.nn)
        for ps in self.proj_strain.values():
            self._et_null_stream += ps

    @property
    def network_null_stream(self):
        """Classical Gursel & Tinto null stream """
        if self._network_null_stream is None:
            self.update_network_null_stream()
        return self._network_null_stream

    @property
    def et_null_stream(self):
        """ET null stream, a plain sum of detector strain response """
        if self._et_null_stream is None:
            
            self.update_et_null_stream()
        return self._et_null_stream

    def add_readable_antenna_pattern_variables(self):
        """Detectors 0, 1, 2 to detectors 1, 2, 3 """
        self.f1p = self.f_p[0]
        self.f1x = self.f_x[0]
        self.f2p = self.f_p[1]
        self.f2x = self.f_x[1]
        self.f3p = self.f_p[2]
        self.f3x = self.f_x[2]

    @property
    def eta(self):
        """(F3x*F1p - F1x*F3p) / (F2p*F3x -  F2x*F3p) """
        return (self.f3x*self.f1p - self.f1x*self.f3p)/\
               (self.f2p*self.f3x - self.f2x*self.f3p)

    @property
    def xi(self):
        """(F1x*F2p - F2x*F1p) / (F2p*F3x - F2x*F3p) """
        return (self.f1x*self.f2p - self.f2x*self.f1p)/\
               (self.f2p*self.f3x - self.f2x*self.f3p)

    @property
    def corrected_strain(self):
        if self._corrected_strain is None:
            self.update_corrected_strain()
        return self._corrected_strain

    def update_corrected_strain(self):
        self._corrected_strain = {}
        for kk, vv in self.strain_interpolants.items():
            self._corrected_strain[kk] = vv(self.time_array[0])

    @property
    def strain_interpolants(self):
        if self._strain_interpolants is None:
            self.update_strain_interpolants()
        return self._strain_interpolants

    def update_strain_interpolants(self):
        self._strain_interpolants = {}
        for kk, coeff in zip([0, 1, 2], [1., -self.eta, -self.xi]):
            self._strain_interpolants[kk] = interp1d(self.time_array[kk] - self.time_delay[kk],
                                                     self.proj_strain[kk]*coeff, fill_value=0.,
                                                     bounds_error=False)

    def __call__(self):
        return self.network_null_stream()

def null_stream(projected_strain, detector):
   """Returns NullStream object for Python package specific input """
   pass
