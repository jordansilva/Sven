#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
from latin.eval_tools.trec_eval import trec_eval
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
# python trec_test.py
#
#

def create_file(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except Exception as exc:
            raise exc

    return open(filename, 'w', 1)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("qrel", help="File with ground-truth result", type=str)
    parser.add_argument("ranks", help="Array with rank files to be evaluated", type=str, nargs='+')
    parser.add_argument("-o", "--output", help="Output path", type=str)
    args = parser.parse_args()

    output_path = ''
    if args.output:
        output_path = args.output

    print "\n##### Trec Stats #####"
    # print(len(args.ranks))
    for rank in args.ranks:
        head, tail = os.path.split(rank)
        path = filter(None, head.split('/'))
        results = trec_eval(args.qrel, rank, params=['-m', 'recsys'])
        
        if len(output_path) == 0:
            output_path = 'nyc/trec/%s.eval' % path[-1]
        fo = create_file('output/%s' % output_path)
        fo.write(results)
        fo.close()

        print('Trec eval generated: %s' % output_path)

    

