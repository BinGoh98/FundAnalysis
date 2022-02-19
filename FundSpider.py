# -*- coding: utf-8 -*-

"""
@Author: BinGoh
@File: FundSpider.py
@Desc: SingleFund 获取单只基金的数据；FundRank 爬取基金排名
@Time: 2022/2/15
"""
import datetime
import json
import math
import os
import re
import pandas as pd

import requests

page_size = 100
log_details = False  # 爬基金数据时是否打印细节


class FundRank(object):
    """
    获取基金排名，并存储在 ./data 目录下

    type_name: 基金类型，可选：混合、债券、股票、指数；默认：全部
    """

    def __init__(self, type_name):
        self.base_url = 'https://fund.eastmoney.com/data/rankhandler.aspx?'
        type_dict = {"混合": "hh", "债券": "zq", "股票": "gp", "指数": "zs"}
        self.type_data = type_dict.get(type_name, "all")

    def getRank(self):
        init_page = 1
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        url = self.base_url + "&op={}&dt={}&ft={}&pi={}&pn={}&sc={}&ed={}".format('ph', 'kf', self.type_data, init_page,
                                                                                  page_size, '6yzf', "2020-10-21")
        header = {"Referer": "https://fund.eastmoney.com/data/fundranking.html", "Host": "fund.eastmoney.com"}
        response = requests.get(url, headers=header).content.decode()

        total_page = int(re.search(r'allPages:([0-9]*),', response).group(1))
        pattern = r'"(.*?)"'
        df = pd.DataFrame()
        # for page in range(1, total_page + 1):
        for page in range(1, 21):
            url = self.base_url + "&op={}&dt={}&ft={}&pi={}&pn={}&sc={}".format('ph', 'kf', self.type_data,
                                                                                      page,
                                                                                      page_size, '6yzf')
            response = requests.get(url, headers=header).content.decode()
            print("正在处理第{}页".format(page))
            it = re.findall(pattern, response)
            for fund in it:
                detail = fund.split(',')
                df = df.append(
                    {
                        "基金代码": str(detail[0]),
                        "基金简称": detail[1],
                        "日期": pd.Timestamp(detail[3]),
                        '日增长率': detail[6],
                        '近一周': detail[7],
                        '近一月': detail[8],
                        '近三月': detail[9],
                        '近六月': detail[10],
                        '近一年': detail[11],
                        '近2年': detail[12],
                        '近3年': detail[13],
                        '今年来': detail[14],
                        '成立来': detail[15]
                    }, ignore_index=True
                )

        columns = ['基金代码', '基金简称', '日期', '日增长率', '近一周', '近一月', '近三月', '近六月', '近一年', '近2年', '近3年', '今年来', '成立来']
        if not os.path.exists("./data"):
            os.mkdir("./data")

        file_name = "./data/FundRank_{}.csv".format(self.type_data)
        df.to_csv(file_name, columns=columns, index=False)
        print('成功获取基金排名，在目录 {}下!'.format(file_name))


class SingleFund(object):
    """
    获取单只基金的数据，存储在 ./data 下

    code: 基金代码
    """

    def __init__(self, code):
        self.code = code
        self.base_url = "http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery1830001140766273019178_1644939075382"

    def getDetail(self):
        init_page = 1
        url = self.base_url + "&fundCode={}&pageIndex={}&pageSize={}".format(self.code, init_page, page_size)
        header = {"Referer": "http://fundf10.eastmoney.com/"}

        response = requests.get(url, headers=header).content.decode()
        json_res = re.match(r'jQuery1830001140766273019178_1644939075382\(([\s\S]*)\)$', response)
        json_res = json_res.group(1)
        dict_res = json.loads(json_res)

        total_count = dict_res['TotalCount']
        total_page = math.ceil(total_count / page_size)
        print("基金代码={}，总页数为 {}".format(self.code, total_page))
        print("=" * 60)

        df = pd.DataFrame()
        for page in range(1, total_page + 1):
            print("正在处理第{}页...".format(page))
            url = self.base_url + "&fundCode={}&pageIndex={}&pageSize={}".format(self.code, page, page_size)
            response = requests.get(url, headers=header).content.decode()
            json_res = re.match(r'jQuery1830001140766273019178_1644939075382\(([\s\S]*)\)$', response)
            json_res = json_res.group(1)
            dict_res = json.loads(json_res)

            daily_data = dict_res['Data']['LSJZList']
            for item in daily_data:
                # 净值日期
                date = item['FSRQ']
                # 单位净值
                unit_net = item['DWJZ']
                # 累计净值
                accumulated_net = item['LJJZ']
                # 日增长率
                daily_growth_rate = "0.00" if item['JZZZL'] == "" else item['JZZZL']

                df = df.append(
                    {
                        "净值日期": pd.Timestamp(date),
                        "单位净值": unit_net,
                        "累计净值": accumulated_net,
                        "日增长率": daily_growth_rate,
                    }, ignore_index=True
                )
                if log_details:
                    print("净值日期=%s, 单位净值=%s, 累计净值=%s, 日增长率=%s" % \
                          (date, unit_net, accumulated_net, daily_growth_rate))

        print("=" * 60)
        df = df.sort_values(by='净值日期', ascending=True)
        df = df.reset_index(drop=True)
        columns = ['净值日期', '单位净值', '累计净值', '日增长率']

        if not os.path.exists("./data"):
            os.mkdir("./data")

        file_name = "./data/" + str(self.code) + ".csv"
        df.to_csv(file_name, columns=columns, index=False)
        print('成功获取代码={} 的基金数据，在目录 {}下!'.format(self.code, file_name))
