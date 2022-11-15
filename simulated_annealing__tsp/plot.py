import matplotlib.pyplot as plt
import time

def plotTSP(paths, points, num_iters=1):
    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    plt.plot(x, y, 'co')
    a_scale = float(max(x))/float(100)
    if num_iters > 1:
        for i in range(1, num_iters):
            xi = []
            yi = []
            for j in paths[i]:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                    head_width = a_scale, color = 'r',
                    length_includes_head = True, ls = 'dashed',
                    width = 0.001/float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                        head_width = a_scale, color = 'r', length_includes_head = True,
                        ls = 'dashed', width = 0.001/float(num_iters))

    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale,
            color ='g', length_includes_head=True)
    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'g', length_includes_head = True)

    plt.xlim(min(x)*1.1, max(x)*1.1)
    plt.ylim(min(y)*1.1, max(y)*1.1)
    plt.show()


class PlotRefresh(object):
    def __init__(self):
        plt.ion()
        self.figure = plt.figure(1)
        self.axes = self.figure.add_subplot(111)

        self.learning_figure = plt.figure(2)
        self.learning_axes = self.learning_figure.add_subplot(111)

        self.figure.show()
        self.learning_figure.show()

    def refresh(self, paths, points, model, iter=1, ):
        x = []
        y = []

        for i in paths[0]:
            x.append(points[i][0])
            y.append(points[i][1])

        self.axes.clear()
        self.axes.plot(x, y, 'co')
        a_scale = float(max(x))/float(100)

        if iter > 1:
            for i in range(1, iter):
                xi = []
                yi = []
                for j in paths[i]:
                    xi.append(points[j][0])
                    yi.append(points[j][1])

                self.axes.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                                head_width=a_scale, color='r',
                                length_includes_head=True, ls='dashed',
                                width=0.001/float(iter))
                for i in range(0, len(x) - 1):
                    self.axes.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                                    head_width=a_scale, color='r', length_includes_head=True,
                                    ls='dashed', width=0.001/float(iter))

        self.axes.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
                        color='g', length_includes_head=True)
        for i in range(0, len(x) - 1):
            self.axes.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width=a_scale,
                            color='g', length_includes_head=True)

        self.axes.set_xlim(min(x)*1.1, max(x)*1.1)
        self.axes.set_ylim(min(y)*1.1, max(y)*1.1)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


        self.learning_axes.clear()
        self.learning_axes.plot([i for i in range(len(model.fitness_list))], model.fitness_list)
        self.learning_figure.canvas.draw()
        self.learning_figure.canvas.flush_events()

        time.sleep(0.0002)



