def null_snr_from_net_and_coherent_snrs(network_snr, coherent_snr):
    return (network_snr**2.0 - coherent_snr**2.0)**0.5


