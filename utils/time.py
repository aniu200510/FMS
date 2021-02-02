# -*- coding:utf-8 -*-
from datetime import datetime, timedelta


class ZTime:
    '''
    Time manager.
    '''

    def __init__(self, tm):
        self.tm = tm

    @property
    def week_start(self):
        return (self.tm-timedelta(days=self.tm.weekday()))

    @property
    def week_end(self):
        return (self.tm+timedelta(days=6-self.tm.weekday()))

    @property
    def month_start(self):
        return datetime(self.tm.year, self.tm.month, 1)

    @property
    def month_end(self):
        return datetime(self.tm.year, self.tm.month+1, 1) - timedelta(days=1)

    @property
    def quarter_start(self):
        month = (self.tm.month-1)-(self.tm.month-1) % 3 + 1
        return datetime(self.tm.year, month,  1)

    @property
    def quarter_end(self):
        month = (self.tm.month-1)-(self.tm.month-1) % 3 + 1
        return datetime(self.tm.year, month+3, 1) - timedelta(days=1)

    @property
    def year_start(self):
        return datetime(self.tm.year, 1, 1)

    @property
    def year_end(self):
        return datetime(self.tm.year+1, 1, 1) - timedelta(days=1)
