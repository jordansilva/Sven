#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

# @Author: @jordansilva
# @Date: September 06, 2016
# @Description:
# Class to generate Graphs with MatplotLib
#
# @Return None
#
# [ Requirements ]
# . Matplotlib
#

dpi = 100

def graph(x, y, title, x_label=None, y_label=None, x_ticks=None,
          y_ticks=None, grid=True, legend=None, filename=None,
          y_lim=None, x_lim=None):

    sns.set_style("whitegrid")
    # plt.rcParams.update({'xtick.labelsize': 8, 'ytick.labelsize': 8})
    sns.set_context("paper")
    # sns.set_palette("colorblind")
    fig = plt.figure(figsize=(9,5))

    n = len(x)+2
    lines = itertools.cycle(('-', '--', ':'))
    # lines = itertools.cycle(('-'))
    color = itertools.cycle(plt.cm.hsv(np.linspace(0, 1, n)))
    marker = itertools.cycle((' ', ' ', ' ', 'o', 'v', '>', 'x', '*',
                              '^', '<', ',', '.', 'p', '*', 'h', 'H',
                              'D', 'd'))

    for x_axis, y_axis, name in zip(x, y, legend):
        plt.plot(x_axis, y_axis, label=name, marker=next(marker),
                 linestyle=next(lines))
        # plt.plot(x_axis, y_axis, linestyle=next(lines),
        #          color=next(color), marker=next(marker),
        #          label=name)

    # Labels
    if y_label:
        plt.ylabel(y_label)

    if x_label:
        plt.xlabel(x_label)

    # Ticks
    if x_ticks:
        plt.xticks(range(1, len(x_ticks)+1), x_ticks)

    if y_ticks:
        plt.y_ticks(range(1, len(y_ticks)+1), y_ticks)

    axes = plt.gca()
    if y_lim:
        axes.set_ylim(y_lim)
    if x_lim:
        axes.set_xlim(x_lim)
    

    # Legend
    if legend:
        plt_legend = plt.legend(loc='best', shadow=True)
        frame = plt_legend.get_frame()
        frame.set_facecolor('0.90')

    if grid:
        plt.grid(True, alpha=0.2)

    # Title
    plt.title(title)
    # plt.figure(figsize=(1024/dpi, 1024/dpi), dpi=dpi)
    if filename is None:
        filename = title

    pp = PdfPages('output/%s.pdf' % filename)
    pp.savefig(fig, dpi=200)
    pp.close()
    plt.close()
    return


def polar(x, y, title, x_label=None, y_label=None, x_ticks=None,
          grid=True, legend=None, filename=None):

    sns.set_style("whitegrid")
    # plt.rcParams.update({'xtick.labelsize': 8, 'ytick.labelsize': 8})
    sns.set_context("paper")
    # sns.set_palette("colorblind")
    fig = plt.figure(figsize=(8,5))

    n = len(x)+2
    lines = itertools.cycle(('-', '--', ':'))
    # lines = itertools.cycle(('-'))
    color = itertools.cycle(plt.cm.hsv(np.linspace(0, 1, n)))
    marker = itertools.cycle((' ', ' ', ' ', 'o', 'v', '>', 'x', '*',
                              '^', '<', ',', '.', 'p', '*', 'h', 'H',
                              'D', 'd'))

    for x_axis, y_axis, name in zip(x, y, legend):
        plt.plot(x_axis, y_axis, label=name, marker=next(marker),
                 linestyle=next(lines))
        # plt.plot(x_axis, y_axis, linestyle=next(lines),
        #          color=next(color), marker=next(marker),
        #          label=name)

    # Labels
    if y_label:
        plt.ylabel(y_label)

    if x_label:
        plt.xlabel(x_label)

    ax = plt.subplot(111, polar=True, axisbg='Azure')
    ax.set_rmax(2.2)

    # Ticks
    if x_ticks:
        plt.xticks(range(1, len(x_ticks)+1), x_ticks)

    # Legend
    # if legend:
    #     plt_legend = plt.legend(loc='best', shadow=True)
    #     frame = plt_legend.get_frame()
    #     frame.set_facecolor('0.90')

    if grid:
        plt.grid(True, alpha=0.2)

    # Title
    plt.title(title)
    plt.polar()
    # plt.figure(figsize=(1024/dpi, 1024/dpi), dpi=dpi)
    if filename is None:
        filename = title

    pp = PdfPages('output/%s.pdf' % filename)
    pp.savefig(fig, dpi=200)
    pp.close()
    plt.close()
    return