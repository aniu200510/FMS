# -*- coding:utf-8 -*-
"""Climb the fund website data."""
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 基金历史净值URL
LSJZ_URL = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?'\
    'type=lsjz&code={0}&page={1}&sdate={2}&edate={3}&per={4}'

# 基金实时信息URL
RT_URL = 'http://fundgz.1234567.com.cn/js/{code}.js?rt=1463558676006'


class FundNetSplider:

    def get_html(self, code, sdate, edate, page=1, per=20):
        url = LSJZ_URL.format(code, page, sdate, edate, per)
        r = requests.get(url)
        html = r.text
        return html

    def get(self, code, sdate, edate, page=1, per=20):
        html = self.get_html(code, sdate, edate, page, per)
        soup = BeautifulSoup(html, 'html.parser')
        # 匹配获取数据的总页数
        pattern = re.compile('pages:(.*),')
        result = re.search(pattern, html).group(1)
        total_page = int(result)

        # 获取表头
        heads = []
        for head in soup.findAll('th'):
            heads.append(head.contents[0])

        data = []
        page_index = 1
        while page_index <= total_page:
            html = self.get_html(code, sdate, edate, page_index, per)
            soup = BeautifulSoup(html, 'html.parser')
            for row in soup.findAll("tbody")[0].findAll("tr"):
                rdata = []
                for r in row.findAll('td'):
                    val = r.contents
                    if val == []:
                        rdata.append(np.nan)
                    else:
                        rdata.append(val[0])

                data.append(rdata)
            page_index += 1

        # 将数据转换为Dataframe对象
        np_data = np.array(data)
        df = pd.DataFrame()
        for col, col_name in enumerate(heads):
            df[col_name] = np_data[:, col]

        # 按照日期排序
        df['净值日期'] = pd.to_datetime(df['净值日期'], format='%Y/%m/%d')
        df = df.sort_values(by='净值日期', axis=0,
                            ascending=True).reset_index(drop=True)
        df = df.set_index('净值日期')

        # 数据类型处理
        df['单位净值'] = df['单位净值'].astype(float)
        df['累计净值'] = df['累计净值'].astype(float)
        df['日增长率'] = df['日增长率'].str.strip('%').astype(float)

        return df


class FundRTSplider:

    def get_html(self, code):
        url = RT_URL.format(code=code)
        r = requests.get(url)
        html = r.text
        return html

    def get(self, code):
        html = self.get_html(code)
        pattern = re.compile(r'jsonpgz\((.*)\);')
        result = re.search(pattern, html).group(1)
        return eval(result)
