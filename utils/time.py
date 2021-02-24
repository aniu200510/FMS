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
        if self.tm.month == 12:
            return datetime(self.tm.year, self.tm.month, 31)
        return datetime(self.tm.year, self.tm.month+1, 1) - timedelta(days=1)

    @property
    def quarter_start(self):
        month = (self.tm.month-1)-(self.tm.month-1) % 3 + 1
        return datetime(self.tm.year, month,  1)

    @property
    def quarter_end(self):
        if self.tm.month < 4:
            month, day = 3, 31
        elif self.tm.month < 7:
            month, day = 6, 30
        elif self.tm.month < 10:
            month, day = 9, 30
        else:
            month, day = 12, 31

        return datetime(self.tm.year, month, day)

    @property
    def year_start(self):
        return datetime(self.tm.year, 1, 1)

    @property
    def year_end(self):
        return datetime(self.tm.year+1, 1, 1) - timedelta(days=1)
