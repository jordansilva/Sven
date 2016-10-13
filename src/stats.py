#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from queries import *
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
training = [['train_1', 'train_2', 'train_3'],
             ['train_2', 'train_3', 'train_4'],
             ['train_3', 'train_4', 'train_5'],
             ['train_4', 'train_5', 'train_6'],
             ['train_5', 'train_6', 'train_7'],
             ['train_6', 'train_7', 'train_8'],
             ['train_7', 'train_8', 'train_9'],
             ['train_8', 'train_9', 'train_10']]
validation = ['test_4', 'test_5', 'test_6', 'test_7', 'test_8', 'test_9', 'test_10', 'test_11']
test = ['test_5', 'test_6', 'test_7', 'test_8', 'test_9', 'test_10', 'test_11', 'test_12']


def generate_stats(filename):
    fo = open(filename, 'w')

    fo.write('Checkins:\t\t\t%s\n' % count_checkins())
    fo.write('Unique Users:\t\t%s\n' % count_users())
    fo.write('Unique Places:\t\t%s\n' % count_venues())

    # TOP 10 Places
    fo.write('\n# TOP 10 Places Checkins\n')
    places = top_checked_places(10)
    for item in places:
        name = item['_id'].encode('utf8')
        fo.write('%d %s\n' % (item['count'], name))

    # TOP 10 Users
    fo.write('\n# TOP 10 Users Checkins\n')
    users = top_checked_users(10)
    for item in users:
        name = item['_id'].encode('utf8')
        fo.write('%d %s\n' % (item['count'], name))

    # Most Checked Places By Time
    items = most_checked_places_timerange()
    fo.write('\n# Most Checked Places by Time\n')
    for key in items:
        item = items[key]
        name = item[1].encode('utf8')
        fo.write('%.2dH - %d %s\n' % (key, item[0], name))

    fo.close()
    return


def generate_graphs():
    # Users & Venues by Fold
    print('Users and Places by Fold')
    users_places_fold(training, validation, test)

    print('Train Validation and Test Folds')
    train_test_fold(training, validation, test)

    print('Distribution Check-ins Time Graph')
    dbs = ['kunkka-rio', 'kunkka-nyc', 'kunkka']
    labels = ['Rio de Janeiro', 'New York', 'Belo Horizonte']
    distribution_checkins_time_graph(dbs, labels)

    print('Categories check-ins per time')
    most_checked_categories_timerange_graph()
    return


def generate_maps():
    # Folds
    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Illegal number of parameters")
        print("stats.py <database>")
        exit(1)

    database = sys.argv[1]

    print "\n##### Stats #####"
    init('host07', database)

    # unique city
    # print('Generating stats')
    # generate_stats('output/%s.txt' % database)

    # multiple cities
    # print('Distribution Checkins Month')
    # distribution_checkins_month()

    # graph
    print('Generating graphs')
    generate_graphs()