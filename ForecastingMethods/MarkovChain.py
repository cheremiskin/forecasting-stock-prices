from ApproximateModels.StaticalModelUsingWalshFunc import StaticalModelUsingWalshFunc
from ForecastingMethods.ForecastingModel import ForecastingModelInterface


class MarkovChain(ForecastingModelInterface):
    levels: list[float] = []
    increments: list[float] = []
    increments_range: float
    increments_in_segments: list[int] = []
    num_of_segments: int
    size_of_segment: float
    inf_segment: list[float] = []

    transition_count_matrix: list[list[int]]
    transition_probability_matrix: list[list[float]]

    counts_transition_from_segment: list[int]

    def __init__(self, data: list[float], num_of_segments: int = 8):
        super().__init__(data)
        self.num_of_segments = num_of_segments
        self.statical_model: list[float] = StaticalModelUsingWalshFunc(
            self.data
        ).get_model()
        self.calculate_walsh_levels()
        self.calculate_increments()
        self.calculate_segments()
        self.allocate_values_to_segments()
        self.fill_transition_count_matrix()
        self.fill_counts_transition_from_segment()
        self.fill_transition_probability_matrix()

        for i in self.transition_probability_matrix:
            print(i)

    def calculate_walsh_levels(self):
        # Если уровни одинаковые подряд ?????
        prev = -1
        for value in self.statical_model:
            if value != prev:
                self.levels.append(value)
                prev = value

    def get_segment_number(self, value):
        """Returns the number of the segment in which the value is located"""
        number = 0
        while number < len(self.inf_segment) and value > self.inf_segment[number]:
            number += 1

        return min(number, self.num_of_segments - 1)

    def calculate_increments(self):
        for i in range(len(self.levels) - 1):
            self.increments.append(self.levels[i + 1] - self.levels[i])

    def calculate_segments(self):
        self.increments_range = max(self.increments) - min(self.increments)
        self.size_of_segment = self.increments_range / self.num_of_segments

        inf = min(self.increments)
        while inf <= max(self.increments) - self.size_of_segment:
            self.inf_segment.append(inf)
            inf += self.size_of_segment

    def allocate_values_to_segments(self):
        for inc_val in self.increments:
            self.increments_in_segments.append(self.get_segment_number(inc_val))

    def fill_transition_count_matrix(self):
        self.transition_count_matrix = [[]] * self.num_of_segments
        for i in range(len(self.transition_count_matrix)):
            self.transition_count_matrix[i] = [0] * self.num_of_segments

        for i in range(len(self.increments_in_segments) - 1):
            prev_segment = self.increments_in_segments[i]
            next_segment = self.increments_in_segments[i + 1]
            self.transition_count_matrix[prev_segment][next_segment] += 1

    def get_count_transition_from_segment(self, segment_index):
        return sum(self.transition_count_matrix[segment_index])

    def fill_counts_transition_from_segment(self):
        self.counts_transition_from_segment = [0] * self.num_of_segments
        for i in range(self.num_of_segments):
            self.counts_transition_from_segment[
                i
            ] = self.get_count_transition_from_segment(i)

    def get_transition_probability(self, source: int, target: int):
        if self.counts_transition_from_segment[source] == 0:
            return 0
        return round(
            self.transition_count_matrix[source][target]
            / self.counts_transition_from_segment[source],
            3,
        )

    def forecast_next_increment(self, current_segment):
        probabilities = self.transition_probability_matrix[current_segment]
        inc = 0

        for i in range(len(probabilities)):
            inc += probabilities[i] * (self.inf_segment[i] + self.size_of_segment / 2)

        return inc

    def fill_transition_probability_matrix(self):
        self.transition_probability_matrix = [[]] * self.num_of_segments
        for i in range(len(self.transition_probability_matrix)):
            self.transition_probability_matrix[i] = [0] * self.num_of_segments

        for source in range(self.num_of_segments):
            for target in range(self.num_of_segments):
                self.transition_probability_matrix[source][
                    target
                ] = self.get_transition_probability(source, target)

    def forecast(self, last_values=None) -> list[float]:
        predicted = []
        last_values = last_values if last_values is not None else self.data

        last_inc = last_values[-1] - self.data[-2]
        last_value = last_values[-1]

        last_segment = self.get_segment_number(last_inc)

        forecast_inc = self.forecast_next_increment(last_segment)
        predicted.append(last_value + forecast_inc)

        return predicted
