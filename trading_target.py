# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:28

@version: python3.5
@author: qiding
"""

import os
import pandas as pd

import log
import my_path

my_log = log.my_log


def get_target(target_path_root, today_str, traded_account_list, id_account_mapping_table):
    data_list = []
    for account in traded_account_list:
        if account != 7:
            file_path = target_path_root + str(account) + '\\' + today_str + '\\final_stock.csv'

            data = pd.read_csv(file_path, encoding='gbk')
            data = data[['coid', 'trade']].rename(columns={'trade': 'target'})
            data['target'] *= 100
        else:
            file_name_list = [file_name_ for file_name_ in os.listdir(target_path_root + str(account)) if file_name_.startswith('final_stock_'+today_str)]
            assert len(file_name_list) == 1
            file_name = file_name_list[0]
            file_path = target_path_root + str(account) + '\\' + file_name

            data = pd.read_csv(file_path, encoding='gbk')
            data = data[['coid', 'trade']].rename(columns={'trade': 'target'})
            data['target'] *= 100

            target_pre = pd.read_csv(my_path.no7_account_root+today_str+'\\adj_data.csv')
            target_pre = target_pre.rename(columns={'code': 'coid'})
            target_pre['trade_tomorrow'] *= 100

            data = pd.merge(target_pre, data, on='coid', how='outer').fillna(0)
            data['target'] = data['target'] + data['trade_tomorrow']
            data = data[['coid', 'target']]

        data['account_name'] = id_account_mapping_table[account]

        my_log.info('read target file: {}'.format(file_path))
        my_log.info('target length: {}'.format(len(data)))

        data_list.append(data)
    data_df = pd.concat(data_list)
    return data_df