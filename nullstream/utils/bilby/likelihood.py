import copy

import numpy as np

from bilby.gw.detector import InterferometerList
from bilby.gw.detector import InterferometerStrainData
from bilby.gw.detector import PowerSpectralDensity
from bilby.gw.likelihood import GravitationalWaveTransient
from bilby.gw.utils import noise_weighted_inner_product

# ================================================================= #
# Einstein Telescope null stream (three almost coincident detectors)
# ================================================================= #

# Likelihood objects

class LikelihoodNullStreamET(GravitationalWaveTransient):
  """Null stream likelihood in the format of the Bilby likelihood. """
  def __init__(self, *args, **kwargs):
    super(NullStreamGWT_v1, self).__init__(*args, **kwargs)
    self.ifos_copy = TriangularWithNullStream(self.interferometers)
    self.fd_null_stream = self.ifos_copy.null_stream.frequency_domain_strain\
                          [self.ifos_copy.null_stream.frequency_mask]
    self.fd_null_stream_psd = self.ifos_copy.null_stream_psd\
                          [self.ifos_copy.null_stream.frequency_mask]
    self.fd_null_stream_dur = self.ifos_copy.null_stream.duration

  def log_likelihood_null_stream(self):
    log_l = 0. # from a residual in null stream (i.e., calibration err., etc.)
    log_l -= 0.5 * noise_weighted_inner_product(self.fd_null_stream, \
                                                self.fd_null_stream, \
                                                self.fd_null_stream_psd, \
                                                self.fd_null_stream_dur)
    return float(np.real(log_l))

# Interferometer objects

class TriangularWithNullStream(InterferometerList):
  def __init__(self, interferometers):
    super(TriangularWithNullStream, self).__init__(interferometers)
    self.null_stream = InterferometerStrainData(
            minimum_frequency=np.min([ifo.minimum_frequency for ifo in self]),
            maximum_frequency=np.max([ifo.maximum_frequency for ifo in self]))
    self.null_stream.sampling_frequency = self[0].sampling_frequency
    self.null_stream.duration = self[0].duration
    self.null_stream.frequency_mask = np.sum([ifo.frequency_mask \
                                              for ifo in self], axis=0, \
                                              dtype=bool)
    self.null_stream_psd = PowerSpectralDensity()
    self.null_stream_psd_f = None

    self.get_null_stream_strain()
    self.get_null_stream_psd()

  def get_null_stream_strain(self):
    """A sum of strain of three detectors is a null stream for ET. For other
    interferometers, this function should be placed to likelihood evaluation,
    and should contain sampled sky positions.
    """
    if self[0].strain_data._frequency_domain_strain is not None:
      print('Setting null stream in frequency domain with masks')
      self.null_stream.frequency_domain_strain = np.sum((\
           ifo.strain_data.frequency_domain_strain\
           for ifo in self))
    elif self[0].strain_data._time_domain_strain is not None:
      print('Setting null stream in time domain (without masks)')
      self.null_stream.time_domain_strain = np.sum((\
           ifo.strain_data.time_domain_strain for ifo in self))

  def get_null_stream_psd(self, sum_psd=True):
    """Options:
    (a) PSD is a sum of three interferometer PSD;
    (b) Calculate PSD from null-stream time series; (results do not look right)
    """
    if sum_psd:
      self.null_stream_psd = copy.copy(self[0].power_spectral_density_array)
      for ii in range(1,3): # adding 2nd and 3d IFO
        self.null_stream_psd += self[ii].power_spectral_density_array 
    else:
      raise ValueError('sum_psd=False seems to yield wrong PSD. To be fixed.')
      self.null_stream_psd_f, self.null_stream_psd = \
                              self.null_stream.create_power_spectral_density(\
                              self.null_stream.duration, name="Null stream")
      print('Make sure that self.null_stream.frequency_array and \
             self.null_stream_psd_f are equal. ', self.null_stream_psd_f, \
             self.null_stream.frequency_array)
