class MatrixEasy:
    @staticmethod
    def dimIsCorrect(matr):
        dim = len(matr[0])
        for row in matr:
            if len(row) != dim:
                return False
        return True

    @staticmethod
    def equalDimensions(matr1, matr2):
        if len(matr1) != len(matr2):
            return False
        for row1, row2 in zip(matr1, matr2):
            if len(row1) != len(row2):
                return False
        return True

    def __init__(self, matr):
        if len(matr) == 0:
            raise RuntimeError("Empty matrix")
        if not self.dimIsCorrect(matr):
            raise RuntimeError("Dimension is not correct")
        self.matrix = matr

    def __add__(self, other):
        if not self.equalDimensions(self.matrix, other.matrix):
            raise RuntimeError("Different dimensions")
        new_matrix = [[a + b for (a, b) in zip(rowS, rowO)]
                      for (rowS, rowO) in zip(self.matrix, other.matrix)]
        return MatrixEasy(new_matrix)

    def __mul__(self, other):
        if not self.equalDimensions(self.matrix, other.matrix):
            raise RuntimeError("Different dimensions")
        new_matrix = [[a * b for (a, b) in zip(rowS, rowO)]
                      for (rowS, rowO) in zip(self.matrix, other.matrix)]
        return MatrixEasy(new_matrix)

    def __matmul__(self, other):
        if len(self.matrix[0]) != len(other.matrix):
            raise RuntimeError("Different dimensions")
        new_matrix = [[0] * len(other.matrix[0]) for i in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(other.matrix[0])):
                for k in range(len(self.matrix[0])):
                    new_matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return MatrixEasy(new_matrix)

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        str = '[\n'
        for row in self.matrix:
            str += ' %s\n' % row
        str += ']'
        return str