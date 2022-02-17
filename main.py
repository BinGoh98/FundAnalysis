# -*- coding: utf-8 -*-

"""
@Author: BinGoh
@File: main.py
@Desc 
@Time: 2022/2/15
"""
from FundSpider import SingleFund, FundRank

if __name__ == '__main__':
    print('start!')
    # 获取基金排名
    rank = FundRank("混合")
    rank.getRank()

    # 获取单只基金数据
    fund = SingleFund('000011')  # 基金code
    fund.getDetail()
