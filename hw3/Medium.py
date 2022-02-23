import numpy as np


class Writer:
    def __str__(self):
        return '%s' % self.matrix


class GetSetClass:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matr):
        self._matrix = np.asarray(matr)


class MatrixM(np.lib.mixins.NDArrayOperatorsMixin, Writer, GetSetClass):
    def __init__(self, matr):
        self._matrix = np.asarray(matr)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        for x in inputs:
            if not isinstance(x, MatrixM):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, MatrixM) else x
                       for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        return None if method == 'at' else type(self)(result)
