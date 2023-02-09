from nullstream.core.timeseries import NullStreamBaseTD

class NullStreamBilbyTD(NullStreamBaseTD):
    """ PyCBC null stream time series object. Calling an instance of
    this object provides network null stream time series data. See
    full description in `nullstream.core.timeseries.NullStreamBaseTD`.

    Parameters
    ==========
    bilby_ifo_list: list, bilby.gw.detector.networks.InterferometerList
        A dict of `bilby.gw.detector.interferometer.Interferometer`,
        with keys corresponding to detector names. It also contains
        strain data, strain projected onto interferometers.
    reference_detector_idx: str
        Index of a detector to which null stream will be referenced to
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
    def __init__(self, bilby_ifo_list, reference_detector_idx,
                 ra_rad=0., dec_rad=0., psi=0., time=0.):
        non_ref_ifo_keys = [kk for kk in range(len(bilby_ifo_list))
                            if kk != reference_detector_idx]
        time_delay_dict = {0: 0.}
        time_array_dict = {0: bilby_ifo_list[reference_detector_idx].time_array}
        projected_strain = {0: bilby_ifo_list[reference_detector_idx].time_domain_strain}
        f_plus_dict = {}
        f_cross_dict = {}
        f_plus_dict[0] = bilby_ifo_list[reference_detector_idx].antenna_response(\
            ra_rad, dec_rad, time, psi, 'plus')
        f_cross_dict[0] = bilby_ifo_list[reference_detector_idx].antenna_response(\
            ra_rad, dec_rad, time, psi,'cross')
        projected_strain = {0: projected_strain_dict[reference_detector_idx]}
        for ii, kk in enumerate(non_ref_ifo_keys):
            projected_strain[ii+1] = bilby_ifo_list[kk].time_domain_strain
            time_delay_dict[ii+1] = bilby.gw.utils.time_delay_geocentric(\
                bilby_ifo_list[kk].geometry.vertex, 
                bilby_ifo_list[reference_detector_idx].geometry.vertex, 
                ra_rad, dec_rad, time)
            time_array_dict[ii+1] = bilby_ifo_list[kk].time_array
            f_plus_dict[ii+1] = bilby_ifo_list[kk].antenna_response(ra_rad, 
                dec_rad, time, psi, 'plus')
            f_cross_dict[ii+1] = bilby_ifo_list[kk].antenna_response(ra_rad, 
                dec_rad, time, psi,'cross')

        super().__init__(projected_strain, time_array_dict, time_delay_dict, 
            f_plus_dict, f_cross_dict)
