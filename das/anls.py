"""Individual fund analysis module."""
from decimal import Decimal

from django.db.models import Max, Min

from oauth.models import FundAccount, FundNet


class FundAnalyst:

    def hold(self, start, end):
        queryset = FundAccount.objects.filter(
            date__gte=start, date__lte=end)

        last_date = queryset.aggregate(Max('date')).get('date__max')

        if not last_date:
            return []

        hold_funds = [dict(
            date=str(last_date),
            principal=q.principal,
            amount=q.amount,
            fund_net=q.fund_net,
            share=q.share,
            fund_name=q.fund.name,
            abbr=q.fund.abbr,
            earnings=round(q.amount-q.principal, 2),
            rate='%.2f%%' % (
                (q.amount-q.principal)*100/q.principal if q.principal else 0)
                ) for q in queryset.filter(date=last_date)]

        return hold_funds

    def profit(self, code, sdate, edate):
        '''
        Calculate the profit of the fund.

        :param code: The fund code.
        :param sdate: Start time of inquiry.
        :param edate: End time of inquiry.

        :return: profit.
        '''
        queryset = FundAccount.objects.filter(date__gte=sdate,
                                              date__lte=edate,
                                              fund__code=code)
        if queryset:
            principal = queryset[0].principal
            amount = queryset[0].amount
            profit = amount - principal

            last_principal = queryset.reverse()[0].principal
            last_amount = queryset.reverse()[0].amount
            last_profit = last_amount - last_principal
            last_queryset = FundAccount.objects.filter(date__lt=sdate,
                                                       fund__code=code)
            if last_queryset:
                last_principal = last_queryset[0].principal
                last_amount = last_queryset[0].amount
                last_profit = last_amount - last_principal

            return float(
                Decimal(str(profit - last_profit)).quantize(Decimal('0.00')))

    def total_profit(self, codes, sdate, edate):
        '''
        Calculate the total profit of the fund.

        :param code: The fund code list.
        :param sdate: Start time of inquiry.
        :param edate: End time of inquiry.

        :return: profit.
        '''
        profits = [self.profit(code, sdate, edate) for code in codes]
        total_profit = sum([p for p in profits if p])
        return float(
            Decimal(str(total_profit)).quantize(Decimal('0.00')))


class FundNetAnalyst:

    def max(self, code, sdate, edate, field='nav'):
        max_nav = FundNet.objects.filter(date__gte=sdate,
                                         date__lte=edate,
                                         fund__code=code).aggregate(
                                             max_net=Max(field))

        return max_nav['max_net']

    def min(self, code, sdate, edate, field='nav'):
        min_nav = FundNet.objects.filter(date__gte=sdate,
                                         date__lte=edate,
                                         fund__code=code).aggregate(
                                             min_net=Min(field))
        return min_nav['min_net']

    def drawdown(self, code, sdate, edate):
        values = FundNet.objects.filter(date__gte=sdate,
                                        date__lte=edate,
                                        fund__code=code).order_by(
                                            'date').values_list('date', 'nav')
        dates = [v[0].strftime("%Y-%m-%d") for v in values]
        navs = [v[1] for v in values]
        drawdown_list = []
        for index, nav in enumerate(navs):
            min_nav = min(navs[index+1:], default=0)
            if min_nav == 0:
                min_nav = nav

            if nav > min_nav:
                drawdown = round((nav-min_nav)/nav, 4)
            else:
                drawdown = 0.0
            drawdown_list.append((dates[index], drawdown))

        return drawdown_list

    def max_drawdown(self, code, sdate, edate):
        '''
        Maximum pullback rate.

        在选定周期内任一历史时点往后推，产品净值走到最低点时的收益率回撤幅度的最大值。

        例：小明10元购入的一只基金涨到了10.2元，继续上涨到12元后，出现下跌，直到6元才停止，后续又上升到9元。
        那么这段时间里小明买基金的最大回撤率就是(6-12)/12≈-50%，最大回撤是50%。
        '''
        data = self.drawdown(code, sdate, edate)
        return max([d[1] for d in data], default=0)

    def drawup(self, code, sdate, edate):
        values = FundNet.objects.filter(date__gte=sdate,
                                        date__lte=edate,
                                        fund__code=code).order_by(
                                            'date').values_list('date', 'nav')
        dates = [v[0].strftime("%Y-%m-%d") for v in values]
        navs = [v[1] for v in values]
        drawup_list = []
        for index, nav in enumerate(navs):
            min_nav = min(navs[:index], default=0)
            if min_nav == 0:
                min_nav = nav

            if nav > min_nav:
                drawup = round((nav-min_nav)/min_nav, 4)
            else:
                drawup = 0
            drawup_list.append((dates[index], drawup))

        return drawup_list

    def max_drawup(self, code, sdate, edate):
        data = self.drawup(code, sdate, edate)
        return max([d[1] for d in data], default=0)

    def roi(self, code, sdate, edate):
        '''
        Calculate the rate of interest the fund net.

        :param code: The fund code.
        :param sdate: Start time of inquiry.
        :param edate: End time of inquiry.

        :return: ROI, Rate of Interest.
        '''
        queryset = FundNet.objects.filter(date__gte=sdate,
                                          date__lte=edate,
                                          fund__code=code)
        if queryset:
            end_net = queryset[0].nav
            start_net = queryset.reverse()[0].nav

            last_queryset = FundNet.objects.filter(date__lt=sdate,
                                                   fund__code=code)
            if last_queryset:
                start_net = last_queryset[0].nav

            roi = (end_net-start_net)/start_net

            return float(Decimal(str(roi)).quantize(Decimal('0.0000')))

    def avg_roi(self, codes, sdate, edate):
        '''
        Calculate the average rate of interest the fund net.

        :param codes: The fund code list.
        :param sdate: Start time of inquiry.
        :param edate: End time of inquiry.

        :return: ROI, Rate of Interest.
        '''
        base = len(codes)
        for code in codes:
            roi = self.roi(code, sdate, edate)
            if roi is not None:
                base += roi

        avg_roi = (base-len(codes))/len(codes)
        return float(Decimal(str(avg_roi)).quantize(Decimal('0.0000')))
