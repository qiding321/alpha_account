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
        # if account != 7:
        file_path = target_path_root + str(account) + '\\final_stock.csv'  # todo
        # file_path = target_path_root + str(account) + '\\' + today_str + '\\final_stock.csv'  # todo
        data = _read_csv(file_path, encoding='gbk')
        data = data[['coid', 'trade']].rename(columns={'trade': 'target'})
        data['target'] *= 100
        # else:
        #     file_name_list = [file_name_ for file_name_ in os.listdir(target_path_root + str(account)) if file_name_.startswith('final_stock_'+today_str)]
        #     if len(file_name_list) != 0:
        #         assert len(file_name_list) == 1
        #         file_name = file_name_list[0]
        #         file_path = target_path_root + str(account) + '\\' + file_name
        #
        #         data = _read_csv(file_path, encoding='gbk')
        #         data = data[['coid', 'trade']].rename(columns={'trade': 'target'})
        #         data['target'] *= 100
        #     else:
        #         file_path = ''
        #         data = pd.DataFrame(columns=['coid', 'target'])
        #
        #     my_log.info('read target file: {}'.format(file_path))
        #     try:
        #         target_pre = _read_csv(my_path.no7_account_root+today_str+'\\adj_data.csv').rename(columns={'trade_tomorrow': 'trade'})
        #         target_pre = target_pre[['coid', 'trade']]
        #         target_pre['trade'] *= 100
        #         # target_pre = target_pre[['coid', 'trade_tomorrow']]
        #     except OSError as os_error:
        #         my_log.error('os error: {}'.format(os_error))
        #         target_pre = pd.DataFrame(columns=['coid', 'trade'])
        #         # target_pre = pd.DataFrame(columns=['coid', 'trade_tomorrow'])
        #
        #     data = pd.merge(target_pre, data, on='coid', how='outer').fillna(0)
        #     data['target'] = data['target'] + data['trade']
        #     # data['target'] = data['target'] + data['trade_tomorrow']
        #     data = data[['coid', 'target']]
        len0 = len(data)
        data = data[pd.notnull(data['coid'])]
        len1 = len(data)
        if len0 != len1:
            my_log.error('prod {} coid nan: {} data, {} nan'.format(account, len0, len0 - len1))

        data['coid'] = data['coid'].apply(lambda x: str(int(x)).zfill(6))
        data['account_name'] = id_account_mapping_table[account]

        my_log.info('target length: {}'.format(len(data)))

        data_list.append(data)
    data_df = pd.concat(data_list)
    return data_df


def _read_csv(target_path, encoding='utf-8'):
    try:
        data = pd.read_csv(target_path, encoding=encoding)
    except UnicodeDecodeError:
        for encoding_ in ['utf-8', 'gbk', 'gb2312']:
            try:
                data = pd.read_csv(target_path, encoding=encoding_)
                flag = 1
            except UnicodeDecodeError:
                flag = 0
            if flag == 0:
                pass
            else:
                break
        if flag == 0:
            raise UnicodeDecodeError
    return data
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        