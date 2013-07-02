#!/usr/bin/python

import datetime
import sys
from socket import gethostbyname

# TODO:
#  - use a smarter (statistics based) downward trend detection algorithm

class Config:
    SENDERSCORE = "%s.score.senderscore.com"
    #SENDERSCORE = "%s.pbl.spamhouse.org"
    LOGFILE="senderscore%s.log"
    # calculate the trend based on this amount of data-points
    TREND_ITEMS = 10
    # warn when the there is a trend change more than the given number
    WARN_ON_TREND_DROP = -5
    # always warn if the trend drops below this threshold
    WARN_MIN_REPUTATION = 10


def get_senderscore(name):
    ip = gethostbyname(name)
    reverse = ip.split(".")
    reverse.reverse()
    reverse = ".".join(reverse)
    score = gethostbyname(Config.SENDERSCORE % reverse).split(".")[-1]
    return score


def do_print_senderscore(name):
    print "%s: %s" % (name, get_senderscore(name))


def get_senderscore_trend(logfile):
    l = []
    with open(logfile) as f:
        for line in f.readlines():
            l.append(line.split("\t"))
    prev_score = int(l[-Config.TREND_ITEMS][2])
    now_score = int(l[-1][2])
    return now_score - prev_score


def do_cron_senderscore(name):
    logfile = Config.LOGFILE % name
    with open(logfile) as f:
        f.write("%s\t%s\t\%s" % (datetime.datetime.now(),
                                 name,
                                 get_senderscore(name)))
    trend = get_senderscore_trend(logfile)
    if (trend < Config.WARN_ON_TREND_DROP or
        trend < Config.WARN_MIN_REPUTATION):
        print "WARNING: Sender score trend '%s'" % trend
    

if __name__ == "__main__":
    if "--cron" in sys.argv:
        do_cron_senderscore(sys.argv[2])
    else:
        do_print_senderscore(sys.argv[1])
