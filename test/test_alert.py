#!/usr/bin/python

import datetime
import unittest

from senderscore import get_senderscore_trend

class AlertTestCase(unittest.TestCase):

    def test_alert(self):
        logfile = "mock_log.log"
        with open(logfile, "w") as f:
            for i in range(10, 100):
                f.write("%s\t%s\t%s\n" % (datetime.datetime.now(),
                                          "foo",
                                          100-i))
        trend = get_senderscore_trend(logfile)
        self.assertEqual(trend, -9)


if __name__ == "__main__":
    unittest.main()
