# -*- coding:utf-8 -*-
from django.test import TestCase

from das.crawler import FundNetSplider, FundRTSplider


class FundSpliderTests(TestCase):

    def test_fundnet_get(self):
        net_20210219 = 2.973
        df = FundNetSplider().get('001875', '2021-02-19', '2021-02-20')
        data = df.values.tolist()
        self.assertEqual(data[0][0], net_20210219)

    def test_fund_rt_get(self):
        code = '005827'
        data = FundRTSplider().get(code)
        self.assertEqual(data['fundcode'], code)
