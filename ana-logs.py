#!/usr/bin/python

import sys

import pandas

import matplotlib
matplotlib.use('GTK') 


if __name__ == "__main__":
    dates = []
    scores = []
    logname = sys.argv[1]
    with open(logname) as f:
        for line in f.readlines():
            date, time, name, score = line.split()
            scores.append(int(score))
            dates.append(date+" "+time)

    s = pandas.Series(scores, index=dates)
    print s.tail(10)
    print s.mean()
    print s.tail(10).mean()
    print s.describe()
    print s.tail(10).pct_change(period=10)
    plot = s.plot()
    plot.set_ylim(0, 100)
    print plot, dir(plot)
    matplotlib.pyplot.savefig("%s.png" % logname)


    # d = {'date': pandas.Series(dates),
    #      'scores': pandas.Series(scores),
    #     }
    # print d
    # df = pandas.DataFrame(d, columns=["Date", "Score"])
    # print df
    # df.pct_change(1)
