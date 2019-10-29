#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # Division in Python 2.7
import matplotlib

# matplotlib.use('Agg')  # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400  # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def interpolate(v, color):
    intervals = np.arange(0, 1.01, 1 / (len(color) - 1))
    for i in range(len(intervals) - 1):
        if intervals[i] <= v <= intervals[i + 1]:
            final = [0, 0, 0]
            for j in range(3):
                final[j] = (color[i + 1][j] - color[i][j]) * ((v - intervals[i]) * (1 / intervals[1])) + color[i][j]
            return final


def hsv2rgb(h, s, v):
    h = (h % 360) / 360
    r, g, b = colors.hsv_to_rgb([h, s, v])
    return r, g, b


def gradient_rgb_bw(v):
    return interpolate(v, [[0, 0, 0], [1, 1, 1]])


def gradient_rgb_gbr(v):
    return interpolate(v, [[0, 1, 0], [0, 0, 1], [1, 0, 0]])


def gradient_rgb_gbr_full(v):
    return interpolate(v, [[0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0]])


def gradient_rgb_wb_custom(v):
    return interpolate(v, [[1, 1, 1], [1, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0]])


def gradient_hsv_bw(v):
    return interpolate(v, [hsv2rgb(0, 0, 0), hsv2rgb(0, 0, 1)])


def gradient_hsv_gbr(v):
    hsv_gbr_array = []
    for i in [120, 180, 240, 300, 360]:
        hsv_gbr_array.append(hsv2rgb(i, 1, 1))
    return interpolate(v, hsv_gbr_array)


def gradient_hsv_unknown(v):

    hsv_unknown_array = []
    for i in [120, 60, 0]:
        hsv_unknown_array.append(hsv2rgb(i, 0.5, 1))
    return interpolate(v, hsv_unknown_array)


def gradient_hsv_custom(v):
    hsv_fun = []
    for i, j in [[42, 0.50], [79, 0.87], [115, 0.40], [224, 0.65], [12, 0.20], [0, 0.70], [98, 0.98], [300, 0.777], [123, 0.456]]:
        hsv_fun.append(hsv2rgb(i, j, 1))
    return interpolate(v, hsv_fun)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()


    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
    plt.show()
