# -*- coding: utf-8 -*-

"""
@Author: BinGoh
@File: main.py
@Desc 
@Time: 2022/2/15
"""
import pandas as pd

from FundSpider import SingleFund, FundRank

if __name__ == '__main__':
    print('start!')
    # 获取基金排名
    # rank = FundRank("")
    # rank.getRank()

    data = pd.read_csv('./data/FundRank_all.csv', dtype={'基金代码': str})
    sort_by_6m = data.sort_values(by='近六月', ascending=False)

    sort_by_6m = data.sort_values(by='近六月', ascending=False)
    names = sort_by_6m[0:10]['基金代码'].tolist()

    for name in names:
        fund = SingleFund(name)  # 基金code
        fund.getDetail()


    # 获取单只基金数据
    # fund = SingleFund('001532')  # 基金code
    # fund.getDetail()
