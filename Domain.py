# -*- coding: utf-8 -*-

"""
@Author: BinGoh
@File: Domain.py
@Desc 
@Time: 2022/2/15
"""


class FundInfo:
    def __init__(self):
        # 基金类型 基金信息字典 基金经理信息字典 当前基金信息类状态（下一步） 需要解析的基金经理列表
        self.fund_kind = 'Unknown'
        self._fund_info = dict()
        self._manager_info = dict()
        self.next_step = 'parsing_fund'
        self.manager_need_process_list = list()
