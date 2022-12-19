from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt

# if plotting does not work comment the following line
matplotlib.use('TkAgg')


class Plotter():

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None, id_=None):
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')
        plt.annotate(id_, xy=(x, y))

    def add_ray(self, xs, ys, kind):
        # plt.plot(xs, ys, label='Ray')
        if kind == 'outside':
            plt.plot(xs, ys, color='r', label='Ray from outside point', linestyle='--', alpha=0.2)
        elif kind == 'boundary':
            plt.plot(xs, ys, color='b', label='Ray from points in boundary', linestyle='-', alpha=0.2)
        elif kind == 'inside':
            plt.plot(xs, ys, color='g', label='Ray from inside point', linestyle='-.', alpha=0.2)
        else:
            plt.plot(xs, ys, color='k', label='Ray from unclassified point', linestyle='--', alpha=0.2)

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='upper left')
        plt.title('Point-in-Polygon Test', fontsize='xx-large', fontweight='bold')
        plt.xlabel('X', fontsize='medium', fontweight='semibold')
        plt.ylabel('Y', fontsize='medium', fontweight='semibold', rotation=90)
        plt.show()
