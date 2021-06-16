from das.crawler import FundNetSplider
from oauth.models import Fund, FundNet


def save_fund_net(code, sdate, edate):
    '''
    Save the fund net between starting time and end time.

    :param code: Fund code.
    :param sdate: Starting time.
    :param edate: End Time.

    :return: None
    '''

    df = FundNetSplider().get(code, sdate, edate)
    try:
        fund = Fund.objects.get(code=code)
    except Fund.DoesNotExist:
        fund = None

    for k, v in zip(df.index.tolist(), df.values.tolist()):
        FundNet.objects.get_or_create(date=k.strftime("%Y-%m-%d"),
                                      nav=v[0], accnav=v[1], naps=v[2],
                                      fund=fund)
