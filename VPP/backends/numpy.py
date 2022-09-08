import operator

import numpy as np

from VPP.backends.backend import BackendHandler


class Numpy(BackendHandler):
    ...

    @classmethod
    def __module(cls):
        return np


@Numpy.handle(np.add)
@Numpy.handle(operator.add)
def handle_add(*inputs, **kwargs):
    return np.add(*inputs, **kwargs)


@Numpy.handle(np.subtract)
@Numpy.handle(operator.sub)
def handle_sub(*inputs, **kwargs):
    return np.subtract(*inputs, **kwargs)
