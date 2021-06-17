import json
import os
from datetime import date, timedelta

from django.db.models import Max

from oauth.models import Fund, FundNet


class Monitor:
    '''Fund monitoring base class.'''
    def __init__(self):
        # Get the project directory.
        base = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        # Configuration file path.
        conf = os.path.join(base, 'etc', 'monitor.json')
        with open(conf) as fp:
            self.conf = json.load(fp)

    def get_cfg(self, code):
        for c in self.conf:
            if c['code'] == code:
                return c

    def check(self, *args, **kwargs):
        pass


class BuyPointMonitor(Monitor):
    '''Fund buy point monitoring.'''

    def check(self, code, valuation):
        '''Monitor if the specified fund reaches the buy point.
        
        :param code: Fund code.
        :param valuation: Fund estimated value.
        
        :return : If the buy point is reached, the difference is returned.
        '''
        cfg = self.get_cfg(code)
        if not cfg:
            return

        today = date.today()
        start_time = today - timedelta(days=cfg.get('period'))
        print('start_time:', start_time)
        queryset = FundNet.objects.filter(
            date__gte=start_time, fund__code=code)

        max_nav = queryset.aggregate(Max('nav')).get('nav__max')
        print('max_nav:', max_nav)
        if not max_nav:
            return

        dvalue = (max_nav - valuation)/max_nav
        if dvalue >= cfg.get('threshold'):
            return dvalue

    def msg(self, code, dvalue):
        '''Get buying Information.
        '''
        fund = Fund.objects.get(code=code)
        return "Fund {abbr} fell by more than {dvalue:.2%}.".format(
            abbr=fund.abbr, dvalue=dvalue)
