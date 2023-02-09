# nullstream

Null stream tools for gravitational wave astronomy

The repository is still at the early stages of development, any contributions are welcome!

## Documentation

Under development. The code is documented with Python docstrings. Run `python setup.py install` to install `nullstream` on your local machine.

At the moment, there are classes with methods to calculate network and ET null stream from detector strain data, as well as `PyCBC` or `Bilby` time series data. There is also null stream likelihood function based on `Bilby` likelihood.

## Citation

The bulk of the code is based on the following work:

> Goncharov, B., Nitz, A.H. and Harms, J., 2022. Utilizing the null stream of the Einstein Telescope. [Physical Review D, 105(12), p.122007](https://doi.org/10.1103/PhysRevD.105.122007). Links: [arXiv:2204.08533](https://arxiv.org/abs/2204.08533), [NASA ADS](https://ui.adsabs.harvard.edu/abs/2022PhRvD.105l2007G).
