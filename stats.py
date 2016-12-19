# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:28

@version: python3.5
@author: qiding
"""

import pandas as pd
import numpy as np


def get_trading_summary(trading_record_today):
    trading_record_today['trading_value'] = trading_record_today['trading_volume'] * trading_record_today['trading_price']
    trading_record_today['trading_value_abs'] = np.abs(trading_record_today['trading_value'])
    trading_record_today['trading_volume_abs'] = np.abs(trading_record_today['trading_volume'])

    trading_record_summary = trading_record_today.groupby(['coid', 'account_name'], as_index=False).sum()
    trading_record_summary['average_price'] = trading_record_summary['trading_value_abs'] / trading_record_summary['trading_volume_abs']

    trading_record_today_drop_0 = trading_record_today[trading_record_today['trading_volume'] != 0]
    first_price = trading_record_today_drop_0.groupby(['coid', 'account_name'], as_index=False).apply(lambda x: x.sort_values(by='time')[['trading_price']].iloc[0, :]).reset_index().rename(columns={'trading_price': 'first_price'})
    trading_record_summary_ = pd.merge(left=first_price, right=trading_record_summary, on=['coid', 'account_name'], how='outer')

    del trading_record_summary_['trading_price']

    trading_record_summary_ = trading_record_summary_.sort_values(by=['account_name'])

    return trading_record_summary_


def get_trading_diff_summary(trading_record_summary, target_today, account_id_mapping_table):
    data_merge = pd.merge(left=trading_record_summary, right=target_today, on=['coid', 'account_name'], how='outer')
    data_merge['target_value'] = data_merge['target'] * data_merge['average_price']
    na_flag = pd.isnull(data_merge['first_price'])
    data_merge_na = data_merge[na_flag]
    data_merge_not_na = data_merge[~na_flag]

    group_by_coid = data_merge_not_na.groupby('account_name')
    key_list = []
    data_list = []
    for key, chunk in group_by_coid:
        chunk_pos = chunk[chunk['target'] >= 0]
        chunk_neg = chunk[chunk['target'] < 0]

        long_trading_value = chunk_pos['trading_value'].sum()
        long_target_value = chunk_pos['target_value'].sum()
        long_cost = ((chunk_pos['average_price'] - chunk_pos['first_price']) * chunk_pos['trading_volume']).sum()
        long_cost_rate = long_cost / np.abs(long_trading_value)

        short_trading_value = chunk_neg['trading_value'].sum()
        short_target_value = chunk_neg['target_value'].sum()
        short_cost = ((-chunk_neg['average_price'] + chunk_neg['first_price']) * chunk_neg['trading_volume'].abs()).sum()
        short_cost_rate = short_cost / np.abs(short_trading_value)

        data_this = pd.Series(
            [long_trading_value, long_target_value, short_trading_value, short_target_value, long_cost, short_cost, long_cost_rate, short_cost_rate],
            index=['long_trading_value', 'long_target_value', 'short_trading_value', 'short_target_value', 'long_cost', 'short_cost', 'long_cost_rate', 'short_cost_rate']
        )
        data_list.append(data_this)
        key_list.append(key)
    data_all_summary = pd.concat(data_list, keys=key_list).unstack()
    data_all_summary = data_all_summary.rename(account_id_mapping_table).reset_index().rename(columns={'index': 'account_name'})
    data_all_summary['long_trading_diff_pct'] = (data_all_summary['long_target_value'] - data_all_summary['long_trading_value']) / data_all_summary['long_target_value']
    data_all_summary['short_trading_diff_pct'] = (data_all_summary['short_target_value'] - data_all_summary['short_trading_value']) / data_all_summary['short_target_value']
    data_all_summary['trading_cost'] = (data_all_summary['long_cost'] + data_all_summary['short_cost']) / (data_all_summary['long_trading_value'].abs() + data_all_summary['short_trading_value'].abs())

    columns_new = [
        'account_name',
        'long_trading_diff_pct', 'short_trading_diff_pct',
        'trading_cost',
        'long_cost_rate', 'short_cost_rate',
        'long_trading_value', 'long_target_value', 'short_trading_value', 'short_target_value',
        'long_cost', 'short_cost',
    ]
    data_all_summary = data_all_summary[columns_new]

    data_all_summary = data_all_summary.sort_values(['account_name'])
    data_merge = data_merge.sort_values(['account_name'])

    return data_all_summary, data_merge
