# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:18

@version: python3.5
@author: qiding
"""

import os
import pandas as pd

import log

my_log = log.my_log


def get_trading_record(trading_record_path):
    file_list = [file_name for file_name in os.listdir(trading_record_path) if file_name.startswith('交易信息')]
    df_list = []
    for file_name in file_list:
        file_path = trading_record_path + file_name
        trading_record_this_file = get_trading_record_one_file(file_path)
        df_list.append(trading_record_this_file)
    data = pd.concat(df_list)
    return data


def get_trading_record_one_file(file_path):
    my_log.info('reading record file: {}'.format(file_path))
    with open(file_path, encoding='utf-8') as f_in:
        record_flag = False
        line_list = []
        for one_line in f_in.readlines():
            if record_flag and len(one_line.replace('\n', '')) == 0:
                record_flag = False
            if record_flag:
                line_list.append(one_line)
            if one_line.replace('\n', '') == '已完成交易':
                record_flag = True
    file_out = os.path.dirname(file_path) + '\\temp.csv'
    with open(file_out, 'w') as f_out:
        f_out.write(''.join(line_list))
    data_raw = pd.read_csv(file_out, encoding='gbk')
    data = data_raw.rename(columns={'账户': 'account_name', '代码': 'coid', '成交价': 'trading_price', '成交量': 'trading_volume', '时间': 'time'})
    data = data[['time', 'account_name', 'coid', 'trading_price', 'trading_volume']]

    my_log.info('data length: {}'.format(len(data)))
    return data
