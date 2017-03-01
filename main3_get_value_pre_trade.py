# -*- coding: utf-8 -*-
"""
Created on 2017/2/14 12:05

@version: python3.5
@author: qiding
"""

import log
import my_path
import trading_info

import datetime
import pandas as pd
import os

this_log = log.my_log


def main():
    traded_account_list = trading_info.traded_account_list
    target_path_root = my_path.target_path_root
    res = dict()
    time_record = dict()
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    # date_str = '20170214'
    for account in traded_account_list:
        file_path = target_path_root + str(account) + '\\' + date_str + '\\' + 'trading_value.csv'
        try:
            data = pd.read_csv(file_path, index_col=False)
            value_dict = _get_value_dict (data)
            res[account] = value_dict
            mtime = os.stat (file_path).st_mtime
            time_record[account] = datetime.datetime.fromtimestamp(mtime)
        except Exception as e:
            this_log.error('error read csv: {}, {}'.format(file_path, e))
    res_df = pd.DataFrame(res).T
    res_df['value_sum'] = res_df['long'].abs() + res_df['short'].abs()
    res_df = res_df.sort_values(by='value_sum')
    this_log.info(res_df)
    this_log.info('\n'.join([str(k)+': '+str(v) for k, v in time_record.items()]))


def _get_value_dict(data):
    data_ = data.dropna()
    long_series = data_['trd'][data_['sign'] == 1]
    short_series = data_['trd'][data_['sign'] == -1]
    
    assert len(long_series) == 1
    assert len(short_series) == 1
    
    long_value = long_series.values[0]
    short_value = short_series.values[0]
    
    res_ = {'long': long_value, 'short': short_value}
    return res_


if __name__ == '__main__':
    main()
