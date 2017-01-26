#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

# @Author: @jordansilva
# @Date: September 05, 2016
# @Description:
# Statistics of database
#
# @Return None
#
# [ Requirements ]
# . MongoClient
#
# [ Usage ]
# python stats.py <database>
#


def precision_at(algorithm, path, folds):
    global db
    x = []

    n = 8
    color = iter(cm.rainbow(np.linspace(0, 1, n)))
    marker = itertools.cycle((' ', ' ', ' ',
                              'o', 'v', '.', 'x', '*',
                              '^', '<',
                              ',', '>', 'p', '*', 'h', 'H', 'D', 'd'))

    for i in xrange(1, folds + 1):
        filename = '%s/fold_%d/trec.txt' % (path, i)
        fo = open(filename, 'r')

        y = []
        for line in fo:
            line = line.split('\t')
            metric = line[0].strip()
            value = line[2].strip().replace('\n', '')

            if 'P_' in metric:
                metric_x = metric.replace('_', '')
                if metric_x not in x:
                    x.append(metric_x)
                y.append(value)

        c = next(color)
        label = 'Fold %s' % i
        plt.plot(range(0, len(y)), y, label=label,
                 color=c, marker=marker.next())

        fo.close()

    # for axis_y, line, label in zip(users, lines, labels):
    #     max_value = max(max_value, max(axis_y))
    #     plt.plot(range(1, len(axis_y)+1), axis_y, linestyle=line,
    #              color='red', label='User ' + label)

    # for axis_y, line, label in zip(venues, lines, labels):
    #     max_value = max(max_value, max(axis_y))
    #     plt.plot(range(1, len(axis_y)+1), axis_y, linestyle=line,
    #              color='blue', label='Venue  ' + label)

    legend = plt.legend(loc='upper right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    plt.xticks(range(0, len(x)), x)
    # # plt.yscale('log')
    # # plt.ylim([0, max_value])
    # plt.ylabel('Precision')
    plt.title(algorithm)
    plt.gca().yaxis.grid(True)
    plt.show()
    # plt.savefig(filename, bbox_inches='tight')
    # plt.show()
    # plt.close()
    return

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Illegal number of parameters")
        print("stats_trec.py <algorithm> <folder> <folds>")
        exit(1)

    algorithm = sys.argv[1]
    path = sys.argv[2]
    folds = int(sys.argv[3])

    print "\n##### Trec Stats #####"
    precision_at(algorithm, path, folds)
