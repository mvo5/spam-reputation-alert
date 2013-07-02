Senderscore reputation alert
============================

A small script that can be run in cron. It will collect the
senderscore reputation score for the given host and can generate
warning mails when the score goes down too fast or if it reaches a low
threshold.

This needs the python-dnspython package.