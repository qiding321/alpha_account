# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:18

@version: python3.5
@author: qiding
"""

import os
import pandas as pd
import datetime

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
    try:
        data_raw = pd.read_csv(file_path)
        # data_raw['time'] = data_raw['time'].apply(lambda s: datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f'))
        # data_raw['time'] = data_raw['time'].apply(lambda s: s.strftime('%H:%M:%S'))
        # data = data_raw.rename(columns={
        #     'accountname': 'account_name',
        #     'stockcode': 'coid',
        #     'tradeprice': 'trading_price',
        #     'tradevol': 'trading_volume',
        #     'time': 'time'
        # })
        data = data_raw.rename(columns={
            '﻿委托时间': 'time',
            # data_raw.columns[0]: 'time',
            '证券代码': 'coid',
            '操作': 'direction',
            '委托数量': 'order_volume',
            '成交数量': 'trading_volume',
            '撤单数量': 'cancel_volume',
            '委托价格': 'order_price',
            '成交均价': 'trading_price',
            '成交时间': 'time',
            '买卖标志': 'direction',
            '成交价格': 'trading_price',
        })
        data['account_name'] = ['mshtong258']*len(data)  # todo
        data['direction'] = data['direction'].apply(lambda s: 1 if s.find('买')>=0 else -1)
        data['trading_volume'] = data['direction'] * data['trading_volume']
        data['status'] = 'transacted'

    except Exception as e:

        with open(file_path, encoding='utf-8') as f_in:
            record_flag = False
            line_list = []
            for one_line in f_in.readlines():
                if record_flag and len(one_line.replace('\n', '')) == 0:
                    record_flag = False
                if record_flag:
                    line_list.append(one_line)
                if one_line.find('已完成交易') >= 0:
                    record_flag = True
        file_out = os.path.dirname(file_path) + '\\temp.csv'
        with open(file_out, 'w') as f_out:
            f_out.write(''.join(line_list))
        data_raw = pd.read_csv(file_out, encoding='gbk')
        data = data_raw.rename(columns={
            '账户': 'account_name', '代码': 'coid',
            '成交价': 'trading_price', '成交量': 'trading_volume',
            '时间': 'time', '委托价': 'order_price', '委托量': 'order_volume',
            '状态': 'status',
        })
        status_map = {'已成': 'transacted', '已撤': 'canceled', '废单': 'invalid'}
        data['status'] = data['status'].apply(lambda x: status_map[x])
        # data['time'] = data['time'].apply(lambda s: datetime.datetime.strptime(s, '%H:%M:%S'))
    data = data[[col_ for col_ in [
        'time', 'account_name', 'coid',
        'trading_price', 'trading_volume', 'order_price',
        'order_volume', 'status',
    ] if col_ in data.columns]]

    data['coid'] = data['coid'].apply(lambda x: str(x).zfill(6))
    my_log.info('data length: {}'.format(len(data)))
    return data


def get_first_price(first_price_path_list):
    data_list = []
    for first_price_path in first_price_path_list:
        if os.path.exists(first_price_path):
            data_tmp = pd.read_csv(first_price_path)\
                .rename(columns={'coid': 'coid', 'accountname': 'account_name'})
            data_tmp = data_tmp[data_tmp['coid'].apply(lambda x: x.__class__ != str or x != 'coid')]
            data_tmp['coid'] = data_tmp['coid'].apply(lambda x: str(x).zfill(6))
            data_tmp = data_tmp.drop_duplicates(subset=['coid', 'account_name'], keep='first')
            data_tmp['nAskPrice1'] = data_tmp['nAskPrice1'].astype(int)
            data_tmp['nBidPrice1'] = data_tmp['nBidPrice1'].astype(int)
            data_list.append(data_tmp)
    data = pd.DataFrame(pd.concat(data_list, ignore_index=True))

    idx_tmp = (data['nAskPrice1'] == 0) & (data['nBidPrice1'] != 0)
    data.loc[idx_tmp, 'nAskPrice1'] = data.loc[idx_tmp, 'nBidPrice1']
    idx_tmp = (data['nAskPrice1'] != 0) & (data['nBidPrice1'] == 0)
    data.loc[idx_tmp, 'nBidPrice1'] = data.loc[idx_tmp, 'nAskPrice1']

    data['first_price'] = (data['nAskPrice1'] + data['nBidPrice1']) / 2 / 10000

    data.loc[data['first_price'] == 0, 'first_price'] = pd.np.nan

    data = data.drop_duplicates(subset=['coid', 'account_name'], keep='first')

    data = data[['coid', 'account_name', 'first_price']].dropna()
    my_log.info('first_price: {}'.format(first_price_path_list))
    return data
