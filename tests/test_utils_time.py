# -*- coding:utf-8 -*-
from datetime import datetime

from django.test import TestCase

from utils.time import ZTime


class ZTimeTests(TestCase):

    def setUp(self):
        self.ztime = ZTime(datetime(2021, 2, 2))

    def test_week_start(self):
        self.assertEqual(self.ztime.week_start,
                         datetime(2021, 2, 1))

    def test_week_end(self):
        self.assertEqual(self.ztime.week_end,
                         datetime(2021, 2, 7))

    def test_month_start(self):
        self.assertEqual(self.ztime.month_start,
                         datetime(2021, 2, 1))

    def test_month_end(self):
        self.assertEqual(self.ztime.month_end,
                         datetime(2021, 2, 28))

    def test_quarter_start(self):
        self.assertEqual(self.ztime.quarter_start,
                         datetime(2021, 1, 1))

    def test_quarter_end(self):
        self.assertEqual(self.ztime.quarter_end,
                         datetime(2021, 3, 31))

    def test_year_start(self):
        self.assertEqual(self.ztime.year_start,
                         datetime(2021, 1, 1))

    def test_year_end(self):
        self.assertEqual(self.ztime.year_end,
                         datetime(2021, 12, 31))
