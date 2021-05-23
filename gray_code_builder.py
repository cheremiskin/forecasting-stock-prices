def get_new_matrix(n, m):
    matrix = [0] * n

    for row in range(n):
        matrix[row] = [0] * m
    return matrix


class GrayCodeBuilder:
    def __init__(self, length=1):
        self.length = 1
        self.size = 2

        self.length_capacity = 1
        self.size_capacity = 2

        self.gray_code = [[0], [1]]

        self.build(length)

    def build(self, new_length):
        """ Generates a gray code of a given length. """
        self.scale(new_length)
        self.fill()

    def scale(self, new_code_length):
        """ Changes the maximum capacity. """
        new_size_capacity = pow(2, new_code_length)

        self.gray_code += ([[0] * (new_code_length - self.length)] * (new_size_capacity - self.size_capacity))
        self.gray_code = list(map(lambda row: ([0] * (new_code_length - self.length_capacity)) + row, self.gray_code))

        self.size_capacity = new_size_capacity
        self.length_capacity = new_code_length

    def fill(self):
        while self.length < self.length_capacity:
            for i in range(self.size):
                self.gray_code[self.size * 2 - i - 1] = self.gray_code[i].copy()
                self.gray_code[i][-(self.length + 1)] = 0
            for i in range(self.size, self.size * 2):
                self.gray_code[i][-(self.length + 1)] = 1

            self.length += 1
            self.size *= 2
