#!/usr/bin/python

import sys

import pandas


if __name__ == "__main__":
    dates = []
    scores = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            date, time, name, score = line.split()
            scores.append(int(score))
            dates.append(date+" "+time)
    s = pandas.Series(scores, index=dates)
    print s.tail(10)
    print s.mean()
