#!/usr/bin/python

import datetime
import sys
from socket import gethostbyname


class Config:
    SENDERSCORE = "%s.score.senderscore.org"
    HOST = "mx1.uni-trier.de"
    LOGFILE="senderscore%s.log"
    TREND_ITEMS = 10


def get_senderscore(name):
    ip = gethostbyname(name)
    reverse = ip.split(".").reverse()
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
    if trend < -5:
        print "WARNING: Sender score trend '%s'" % trend
    

if __name__ == "__main__":
    if "--print" in sys.argv:
        do_print_senderscore(sys.argv[2])
    elif "--cron" in sys.argv:
        do_cron_senderscore(sys.argv[2])
