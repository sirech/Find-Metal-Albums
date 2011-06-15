# -*- coding: utf-8 -*-
from test_base import BaseTest
from metalfinder.notify import Notifier, date_and_next_day

from mock import patch, Mock

from datetime import datetime

class NotifyTest(BaseTest):

    def setUp(self):
        super(NotifyTest,self).setUp()


    def test_date_and_next(self):
        self.assertEqual(date_and_next_day(datetime(year=2011, month=6, day=25)), ('2011-06-25', '2011-06-26'))

    def test_date_and_next_edge(self):
        self.assertEqual(date_and_next_day(datetime(year=2011, month=12, day=31)), ('2011-12-31', '2012-01-01'))

