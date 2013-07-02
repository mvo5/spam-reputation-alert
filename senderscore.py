#!/usr/bin/python

import datetime
import sys
from socket import gethostbyname

# TODO:
#  - use a smarter (statistics based) downward trend detection algorithm

class Config:
    SENDERSCORE = "%s.score.senderscore.com"
    #SENDERSCORE = "%s.pbl.spamhouse.org"
    LOGFILE="senderscore-%s.log"
    # calculate the trend based on this amount of data-points
    TREND_ITEMS = 10
    # warn when the there is a trend change more than the given number
    WARN_ON_TREND_DROP = -5
    # always warn if the trend drops below this threshold
    WARN_MIN_REPUTATION = 10
    # the resolver needs to be external
    RESOLVER = "8.8.8.8"


def get_senderscore(name):
    import dns.resolver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [Config.RESOLVER]
    ip = resolver.query(name)[0].to_text()
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
    if len(l) < Config.TREND_ITEMS:
        return 0
    prev_score = int(l[-Config.TREND_ITEMS][2])
    now_score = int(l[-1][2])
    return now_score - prev_score


def do_cron_senderscore(name):
    logfile = Config.LOGFILE % name
    now_score = get_senderscore(name)
    with open(logfile, "a") as f:
        f.write("%s\t%s\t%s\n" % (datetime.datetime.now(),
                                 name,
                                 now_score))
    trend = get_senderscore_trend(logfile)
    if (trend < Config.WARN_ON_TREND_DROP or
        now_score < Config.WARN_MIN_REPUTATION):
        print "WARNING: Sender score trend '%s'" % trend
    

if __name__ == "__main__":
    if "--cron" in sys.argv:
        do_cron_senderscore(sys.argv[2])
    else:
        do_print_senderscore(sys.argv[1])
