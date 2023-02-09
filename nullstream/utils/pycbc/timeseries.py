from nullstream.core.timeseries import NullStreamBaseTD

class NullStreamPycbcTD(NullStreamBaseTD):
    """ PyCBC null stream time series object. Calling an instance of
    this object provides network null stream time series data. See 
    full description in `nullstream.core.timeseries.NullStreamBaseTD`.

    Parameters
    ==========
    projected_strain_dict: dict
        A dict of `pycbc.types.timeseries.TimeSeries`, with keys
        corresponding to detector names.
    pycbc_detector_dict: dict
        A dict of `pycbc.detector.Detector`.
    reference_detector_key: str
        Key of a detector to which null stream will be referenced to
        (time delays)
    ra_rad: float, optional
        Right ascention of a gravitational wave source, with respect to
        which null stream will be constructed. Not required for
        ET null stream.
    dec_rad: float, optional
        Declination of a gravitational wave source, with respect to
        which null stream will be constructed. Not required for
        ET null stream.
    psi: float, optional
        Polarization of a gravitational wave source, with respect to
        which null stream will be constructed. Not required for 
        ET null stream.
    time: float, optional
        Time with respect to which time delays between detectors
        and antenna patterns will be calculated.

    Returns
    =======
    network_null_stream: `numpy.ndarray`
        Sky position dependent network null stream
    et_null_stream: `numpy.ndarray`
        ET null stream independent of gravitational wave source 
        parameters
    """
    def __init__(self, projected_strain_dict, pycbc_detector_dict, reference_detector_key, 
                 ra_rad=0., dec_rad=0., psi=0., time=0.):
        non_ref_ifo_keys = [kk for kk in pycbc_detector_dict.keys()
                            if kk != reference_detector_key]
        time_delay_dict = {0: 0.}
        time_array_dict = {0: projected_strain_dict[reference_detector_key].sample_times}
        f_plus_dict = {}
        f_cross_dict = {}
        f_plus_dict[0], f_cross_dict[0] = detectors[reference_detector_key].\
                                          antenna_pattern(ra_rad, dec_rad, psi, time)
        projected_strain = {0: projected_strain_dict[reference_detector_key]}
        for ii, kk in enumerate(non_ref_ifo_keys):
            projected_strain[ii+1] = projected_strain_dict[kk]
            time_delay_dict[ii+1] = detectors[kk].time_delay_from_detector(\
                                  detectors[reference_detector_key], ra_rad, dec_rad, time)
            time_array_dict[ii+1] = projected_strain_dict[kk].sample_times
            f_plus_dict[ii+1], f_cross_dict[ii+1] = detectors[kk].antenna_pattern(\
                                                ra_rad, dec_rad, psi, 0)

        super().__init__(projected_strain, time_array_dict, time_delay_dict, f_plus_dict, f_cross_dict)
