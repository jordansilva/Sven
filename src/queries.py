#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import graph
import json
from pymongo import MongoClient
from datetime import datetime

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


# Initialize Database
def init(host, database):
    global client, db
    client = MongoClient(host)
    db = client[database]
    return


# Sample of check-ins over earth (Tweets around the earth - crawler chapter)
# Most checked places by season (Characterization)
# Number of users & places cold-start by month (Evaluation)
# Cumulative test size history by month (Evaluation)
# Training & test data coverage on the map (Evaluation)
# Measure the amount of check-ins in the streets and neighborhoods

# Most checked categories by time range (Characterization)
def most_checked_categories_timerange():
    result = db['cache'].find({'query': 'most_checked_categories_timerange'})
    if result.count() == 0:
        result = db['swarm'].aggregate([{
                                          '$project': {
                                            'ISODate': {
                                              '$add': [datetime.utcfromtimestamp(0),
                                                       {'$multiply': [1000,
                                                        '$swarm.checkin.createdAt']
                                                        }]
                                            },
                                            'name':
                                            '$swarm.venue.main_category.name'
                                          }
                                        }, {
                                          '$project': {
                                            'hour': {
                                              '$dateToString': {
                                                'format': '%HH',
                                                'date': '$ISODate'
                                              }
                                            },
                                            'name': '$name'
                                          }
                                        },
                                        {
                                          '$group': {
                                            '_id': {
                                             'hour': '$hour',
                                             'category': '$name'
                                             },
                                            'count': {
                                              '$sum': 1
                                            }
                                          }
                                        },
                                        {'$sort':
                                         {'_id.hour': 1,
                                          '_id.category': 1
                                          }
                                         }])

        items = []
        for r in result:
            hour = int(r['_id']['hour'].replace('H', ''))
            if 'category' not in r['_id']:
                name = 'Null'
            else:
                name = r['_id']['category']
            count = r['count']
            items.append((hour, count, name))

        items.sort(key=lambda tup: tup[0])

        db['cache'].insert({'query': 'most_checked_categories_timerange',
                            'result': json.dumps(items)})
    else:
        items = json.loads(result[0]['result'])

    return items


# Most checked places by time range (Characterization)
def most_checked_places_timerange():
    result = db['swarm'].aggregate([{
                                      '$project': {
                                        'ISODate': {
                                         '$add': [datetime.utcfromtimestamp(0),
                                                   {'$multiply': [1000,
                                                    '$swarm.checkin.createdAt']
                                                    }]
                                        },
                                        'name': '$swarm.venue.name'
                                      }
                                    }, {
                                      '$project': {
                                        'hour': {
                                          '$dateToString': {
                                            'format': '%HH',
                                            'date': '$ISODate'
                                          }
                                        },
                                        'name': '$name'
                                      }
                                    },
                                    {
                                      '$group': {
                                        '_id': {'$concat':
                                                ['$hour', '::', '$name']},
                                        'count': {
                                          '$sum': 1
                                        }
                                      }
                                    },
                                    {'$sort': {'count': -1}}])

    items = {}
    for r in result:
        item = r['_id'].split('::')
        hour = int(item[0].replace('H', ''))
        if hour not in items:
            items[hour] = (r['count'], item[1])

    return items


# Distribution of check-ins by month and city (Characterization)
def distribution_checkins_month():
    result = db['cache'].find({'query': 'distribution_checkins_month'})
    if result.count() == 0:
        result = db['swarm'].aggregate([{'$project': {'ISODate':
                                       {'$add': [datetime.utcfromtimestamp(0),
                                        {'$multiply':
                                         [1000, '$swarm.checkin.createdAt']}
                                       ]}}},
                                       {'$project': {'yearMonthDay':
                                        {'$dateToString':
                                         {'format': '%Y-%m',
                                          'date': '$ISODate'}}}},
                                       {'$group': {'_id': '$yearMonthDay',
                                                   'count': {'$sum': 1}}}])
        items = {}
        for r in result:
            items[r['_id']] = r['count']

        db['cache'].insert({'query': 'distribution_checkins_month',
                            'result': json.dumps(items)})
    else:
        items = json.loads(result[0]['result'])

    return items


# Quantity of Check-ins by time (Characterization)
def distribution_checkins_time():
    result = db['cache'].find({'query': 'distribution_checkins_time'})
    if result.count() == 0:
        result = db['swarm'].aggregate([{'$project': {'ISODate':
                                       {'$add': [datetime.utcfromtimestamp(0),
                                        {'$multiply':
                                         [1000, '$swarm.checkin.createdAt']}
                                       ]}}},
                                       {'$project': {'yearMonthDay':
                                        {'$dateToString':
                                         {'format': '%HH',
                                          'date': '$ISODate'}}}},
                                       {'$group': {'_id': '$yearMonthDay',
                                                   'count': {'$sum': 1}}},
                                       {'$sort': {'_id': 1}}])

        items = {}
        for r in result:
            iid = int(r['_id'].replace('H', ''))
            items[iid] = r['count']

        db['cache'].insert({'query': 'distribution_checkins_time',
                            'result': json.dumps(items)})
    else:
        items = json.loads(result[0]['result'])

    return items


# Top checked places (Characterization)
def top_checked_places(limit):
    result = db['cache'].find({'query': 'top_checked_places_' + str(limit)})
    if result.count() == 0:
        result = db['swarm'].aggregate([{'$group': {'_id': '$swarm.venue.name',
                                       'count': {'$sum': 1}}},
                                       {'$sort': {'count': -1}}])

        i = 1
        items = []
        for r in result:
            items.append(r)
            if i >= limit:
                break
            i += 1
        db['cache'].insert({'query': 'top_checked_places_' + str(limit),
                            'result': json.dumps(items)})
    else:
        items = json.loads(result[0]['result'])

    return items


# Top checked users (Characterization)
def top_checked_users(limit):
    result = db['cache'].find({'query': 'top_checked_users_' + str(limit)})
    if result.count() == 0:
        result = db['swarm'].aggregate([{'$group':
                                        {'_id': '$swarm.checkin.user.canonicalUrl',
                                         'count': {'$sum': 1}}},
                                       {'$sort': {'count': -1}}])

        i = 1
        items = []
        for r in result:
            items.append(r)
            if i >= limit:
                break
            i += 1

        db['cache'].insert({'query': 'top_checked_users_' + str(limit),
                            'result': json.dumps(items)})
    else:
        items = json.loads(result[0]['result'])

    return items


# Quantity of Check-ins, Users and Places (Characterization)
def count_checkins():
    result = db['swarm'].count()
    return result


def count_users():
    result = db['swarm'].distinct('swarm.checkin.user.id')
    return len(result)


def count_venues():
    result = db['swarm'].distinct('swarm.venue.id')
    return len(result)


# Number of train & tests by fold (Evaluation)
def train_test_fold(train_data, validation_data, test_data):
    data1 = []
    data2 = []
    data3 = []

    for training, validation, test in zip(train_data, validation_data, test_data):
        r1 = 0
        for t in training:
            r1 += db[t].count()

        r2 = db[validation].count()
        r3 = db[test].count()

        data1.append(r1)
        data2.append(r2)
        data3.append(r3)

    items = (data1, data2, data3)
    n = len(items[0])
    X = [list(range(1, n+1))] * len(items)
    Y = items

    legend = ['Training', 'Validation', 'Test']
    graph.graph(x=X, y=Y, title='Training & Test Check-ins',
                x_label='# Fold', y_label='# Cases',
                legend=legend, filename='training-fold')

    return


# Number of users & places training and test by fold (Evaluation)
def users_places_fold(train_data, validation_data, test_data):
    training_U = []
    validation_U = []
    test_U = []
    training_V = []
    validation_V = []
    test_V = []

    for training, validation, test in zip(train_data, validation_data, test_data):
        u1 = 0
        v1 = 0
        for t in training:
            u1 += len(db[t].distinct('user'))
            v1 += len(db[t].distinct('venue'))

        u2 = len(db[validation].distinct('user'))
        v2 = len(db[validation].distinct('venue'))

        u3 = len(db[test].distinct('user'))
        v3 = len(db[test].distinct('venue'))

        training_U.append(u1)
        validation_U.append(u2)
        test_U.append(u3)

        training_V.append(v1)
        validation_V.append(v2)
        test_V.append(v3)

    items = (training_U, validation_U, test_U) + (training_V, validation_V, test_V)
    n = len(items[0])
    X = [list(range(1, n+1))] * len(items)
    Y = items

    legend = ['User Training', 'User Validation', 'User Test',
              'Venue Training', 'Venue Validation', 'Venue Test']
    graph.graph(x=X, y=Y, title='Training & Test Check-ins',
                x_label='# Fold', y_label='# Cases',
                legend=legend, filename='training-users-venues-fold')

    return


def distribution_checkins_time_graph(databases, labels):
    global db

    X_ticks = ['5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H', '14H',
               '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H',
               '0H', '1H', '2H', '3H', '4H']
    Y = []

    for db_name in databases:
        db = client[db_name]
        result = distribution_checkins_time()

        yt = [None] * len(X_ticks)
        for key in result:
            ind = X_ticks.index(str(key) + 'H')
            yt[ind] = result[key]

        Y.append(yt)

    n = len(Y[0])
    X = [list(range(1, n+1))] * len(Y)

    graph.graph(x=X, y=Y, title='Distribution Check-ins per Hour',
                x_label='Time period', y_label='Check-ins',
                x_ticks=X_ticks, legend=labels, filename='dist-checkins-time')

    return


def most_checked_categories_timerange_graph():
    X_ticks = ['5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H', '14H',
               '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H',
               '0H', '1H', '2H', '3H', '4H']
    Y_temp = {}
    labels = []
    y_max = 0

    result = most_checked_categories_timerange()
    for key, count, name in result:
        if name == 'Null':
            continue

        if name not in Y_temp:
            Y_temp[name] = [None] * len(X_ticks)
            labels.append(name)

        ind = X_ticks.index(str(key) + 'H')
        Y_temp[name][ind] = count
        if count > y_max:
            y_max = count

    Y = []

    for yt in Y_temp:
        Y.append(Y_temp[yt])

    n = len(Y[0])
    X = [list(range(1, n+1))] * len(Y)

    graph.graph(x=X, y=Y, title='Categories Check-ins per Hour',
                x_label='Time period', y_label='Check-ins',
                x_ticks=X_ticks, legend=labels, filename='most_checked_categories',
                y_lim=[0, y_max+1000])

    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Illegal number of parameters")
        print("queries.py <database>")
        exit(1)

    database = sys.argv[1]

    init('localhost', database)

    # multiple cities
    # distribution_checkins_month()

    # Most checkins time graph
    print most_checked_categories_timerange()
