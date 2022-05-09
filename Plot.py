import matplotlib.pyplot as plt


class PlotMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Plot(metaclass=PlotMeta):
    plots = []

    def plot(self, data):
        self.plots.append(data)

    def show(self, orientation="vertical"):
        num_of_plots = len(self.plots)

        for i in range(len(self.plots)):
            if orientation == "vertical":
                plt.subplot(num_of_plots, 1, i + 1)
            else:
                plt.subplot(1, num_of_plots, i + 1)
            plt.plot(self.plots[i])

        plt.show()
