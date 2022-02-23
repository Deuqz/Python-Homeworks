from Easy import MatrixEasy


class Hasher:
    MOD = 10 ** 9 + 7
    p = 73

    def __eq__(self, other):
        if not MatrixE.equalDimensions(self.matrix , other.matrix):
            return False
        for (rowS, rowO) in zip(self.matrix, other.matrix):
            for (a, b) in zip(rowS, rowO):
                if a != b:
                    return False
        return True

    # Хэш-функция представляет все элементы матрицы в виде многочлена
    # a_{n - 1, n - 1} + a_{n -1, n - 2}x + ...
    # и считает его значение в точке 2 по модулю 10^9 + 7
    def __hash__(self):
        h = 0
        for row in self.matrix:
            for a in row:
                h = (h * self.p + a) % self.MOD
        return h


class MatrixHard(MatrixEasy, Hasher):
    _matrix_hashes = dict()

    def __matmul__(self, other):
        h1, h2 = self.__hash__(), other.__hash__()
        if (h1, h2) not in self._matrix_hashes:
            self._matrix_hashes[(h1, h2)] = super(MatrixHard, self).__matmul__(other)
        return self._matrix_hashes[(h1, h2)]
