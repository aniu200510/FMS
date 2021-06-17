from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail

from das.crawler import FundRTSplider
from das.db import save_fund_net
from das.monitor import BuyPointMonitor
from fms.celery import app
from oauth.models import Fund, FundAccount, FundNet


@app.task
def save_fund_net_by_day(day=7):
    today = date.today()
    edate = today.strftime("%Y-%m-%d")
    days_ago = today - timedelta(days=day)
    sdate = days_ago.strftime("%Y-%m-%d")

    codes = Fund.objects.all().values_list('code', flat=True)
    for code in codes:
        try:
            save_fund_net(code, sdate, edate)
        except Exception:
            continue


@app.task
def save_fund_account_by_day():
    last_date = FundAccount.objects.all().first().date
    queryset = FundAccount.objects.filter(date=last_date)
    for q in queryset:
        for net in FundNet.objects.filter(fund=q.fund, date__gt=last_date):
            amount = round(q.share * net.nav, 2)
            FundAccount.objects.get_or_create(date=net.date,
                                              principal=q.principal,
                                              amount=amount,
                                              fund_net=net.nav,
                                              share=q.share,
                                              fund=q.fund)


@app.task
def monitoring_fund_buy_point():
    monitor = BuyPointMonitor()
    messages = list()
    for cfg in monitor.conf:
        try:
            data = FundRTSplider().get(cfg['code'])
        except Exception:
            continue

        dvalue = monitor.check(cfg['code'], float(data['gsz']))
        if bool(dvalue):
            messages.append(monitor.msg(cfg['code'], dvalue))

    if messages:
        send_mail("【FUND BUY POINT】",
                  '\n'.join(messages),
                  settings.EMAIL_FROM,
                  settings.RECIPIENT_LIST,
                  fail_silently=False)
