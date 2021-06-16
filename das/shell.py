from datetime import datetime

from django.db.models import Max, Sum

from das.anls import FundNetAnalyst
from das.crawler import FundRTSplider
from oauth.models import Fund, FundAccount, FundNet
from utils.time import ZTime


def rt_fund(code=None):
    queryset = FundAccount.objects.all()
    last_date = queryset.aggregate(Max('date')).get('date__max')
    holds = queryset.filter(date=last_date)
    fmt = '\033[1;30m|{:18}|{:16}' + '|{:10}'*13+'|\033[0m'
    # {:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|'
    # 日期 名称缩写 代码
    # 年最大净值 年最小净值 净值
    # 估值 预期涨幅 年最大涨幅
    # 置位度(估值在年最大净值值和最小净值间的位置) 份额 本金
    # 金额 预估金额 收益
    #
    # EPS (Earning Per Share),每股收益即每股盈利（EPS），又称每股税后利润、每股盈余，
    # 指税后利润与股本总数的比率.
    title = fmt.format('DATE', 'ABBR', 'CODE',
                       'MAXNAV', 'MINNAV', 'NAV',
                       'ESTIMATE', 'PGR', 'MGR',
                       'PDOP', 'SHARE', 'PRINCIPAL',
                       'AMOUNT', 'VALUATION', 'EPS',
                       )
    print('\033[1;30m' + '-' * 182 + '\033[0m')
    print(title)
    total = 0
    total1 = 0
    total2 = 0
    for d in holds:
        data = FundRTSplider().get(d.fund.code)
        sdate = ZTime(datetime.today()).year_start.strftime("%Y-%m-%d")
        edate = ZTime(datetime.today()).year_end.strftime("%Y-%m-%d")
        max_nav = FundNetAnalyst().max(d.fund.code, sdate, edate)
        min_nav = FundNetAnalyst().min(d.fund.code, sdate, edate)

        net = FundNet.objects.filter(fund=d.fund).first()
        # 估算累加净值
        gs_accnav = float(data['gsz']) + (net.accnav - net.nav)
        max_accnav = FundNetAnalyst().max(d.fund.code, sdate, edate, 'accnav')
        min_accnav = FundNetAnalyst().min(d.fund.code, sdate, edate, 'accnav')
        # 置位度 =（预估累加净值 - 当年累加净值最小值）/(当年累加净值最大值-当年累加净值最小值)
        pdop = round((gs_accnav-min_accnav)/(max_accnav-min_accnav), 4)
        valuation = round(d.share * float(data['gsz']), 2)
        mgr = round((max_nav - min_nav) / max_nav, 4)
        fund_fmt = fmt.format(data['gztime'], d.fund.abbr, data['fundcode'],
                              str(max_nav), str(min_nav), data['dwjz'],
                              data['gsz'], '{:.2%}'.format(
                                  float(data['gszzl'])/100),
                              '{:.2%}'.format(mgr),
                              '{:.2%}'.format(pdop),
                              str(d.share), str(d.principal),
                              str(d.amount), str(valuation),
                              str(round(valuation-d.amount, 2)))
        print('\033[1;30m' + '-' * 182 + '\033[0m')
        print(fund_fmt)
        total += valuation
        total1 += d.principal
        total2 += d.amount
    print('\033[1;30m' + '-' * 182 + '\033[0m')
    print('\033[1;30mTOTAL EPS:{} \033[0m'.format(round(total-total2, 2)))
    print('\033[1;30mTOTAL VALUATION:{} \033[0m'.format(round(total, 2)))
    print('\033[1;30mTOTAL TOTAL PRINCIPAL:{} \033[0m'.format(round(total1, 2)))
    print('\033[1;30mTOTAL AMOUNT:{} \033[0m'.format(round(total2, 2)))


def stat_fund(sdate='2021-01-01', edate='2022-01-01'):
    queryset = FundAccount.objects.all()
    dates = queryset.values_list('date', flat=True).distinct()
    fmt = '\033[1;30m' + '|{:12}'*6 + '|\033[0m'
    title = fmt.format('DATE', 'PRINCIPAL', 'AMOUNT',
                       'EARNINGS', 'RE', 'RET')
    print(title)
    yday_eps = 0
    for d in dates.reverse():
        total_principal = queryset.filter(
            date=d).aggregate(bj=Sum('principal'))['bj']
        total_amount = queryset.filter(
            date=d).aggregate(je=Sum('amount'))['je']
        today_eps = round(total_amount - total_principal, 2)
        growth = round(today_eps - yday_eps, 2)
        ret = growth / (total_amount-growth)
        print(fmt.format(str(d), total_principal, total_amount,
                         today_eps, growth, '{:.2%}'.format(ret)))
        yday_eps = today_eps


def show_draw(sdate='2021-02-01', edate='2021-02-23'):
    funds = Fund.objects.all()
    fmt = 'NAME:{:20} UP:{:.2%} DOWN:{:.2%}'
    for fund in funds:
        up = FundNetAnalyst().max_drawup(fund.code, sdate, edate)
        down = FundNetAnalyst().max_drawdown(fund.code, sdate, edate)
        print(fmt.format(fund.abbr, up, down))


def show(year):
    from datetime import datetime
    from utils.time import ZTime

    tm = datetime(year, 1, 1)
    start = ZTime(tm).year_start.strftime("%Y-%m-%d")
    end = ZTime(tm).year_end.strftime("%Y-%m-%d")
    print(start, '--------->', end)
    show_draw(start, end)

    for quarter in (1, 4, 7, 10):
        tm = datetime(year, quarter, 1)
        start = ZTime(tm).quarter_start.strftime("%Y-%m-%d")
        end = ZTime(tm).quarter_end.strftime("%Y-%m-%d")
        print(start, '**********>', end)
        show_draw(start, end)

    for month in range(1, 13):
        tm = datetime(year, month, 1)
        start = ZTime(tm).month_start.strftime("%Y-%m-%d")
        end = ZTime(tm).month_end.strftime("%Y-%m-%d")
        print(start, '===========>', end)
        show_draw(start, end)
