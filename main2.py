# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:05

@version: python3.5
@author: qiding

@files in:
trading record: \\\\SHIMING\\trading\\trading_summary\\today_str
target: \\\\SHIMING\\trading\\target_files
target No.7 adj E:\\MyTrading\\IntradayAccount\\Account\\No7DailyAccount\\today_str\\adj_data.csv

@files out:
E:\\MyTrading\\IntradayAccount\\Account\\AlphaAccountDailySummary\\today_str\\trading_summary.csv
E:\\MyTrading\\IntradayAccount\\Account\\AlphaAccountDailySummary\\today_str\\ttrading_detail.csv
E:\\MyTrading\\IntradayAccount\\Account\\AlphaAccountDailySummary\\today_str\\tdata_merge_all.csv
"""

import os
import datetime

import my_path
import log
import mail
import trading_record
import trading_target
import stats

import trading_info

my_log = log.my_log


def main():
    # traded_account_list = [1, 2, 4, 5, 7, 8, 10, 11, 16, 19, 101, 102, 107, 203, 208, 301]

    traded_account_list = trading_info.traded_account_list
    id_account_mapping_table = trading_info.id_account_mapping_table

    account_id_mapping_table = dict(zip(id_account_mapping_table.values(), id_account_mapping_table.keys()))

    # ========================= date and log ==========================
    today = datetime.datetime.now()
    # today = datetime.datetime(2016,1,4)
    today_str = today.strftime('%Y%m%d')
    my_log.info('Alpha Daily Trading Account Begin @ {}'.format(today))
    my_log.info('trading account: {}'.format(','.join(str(t_) for t_ in traded_account_list)))

    # ========================= path ==========================
    output_path = my_path.output_path_root + today_str + '\\'
    output_path2 = my_path.output_path_root2 + today_str + '\\'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(output_path2):
        os.makedirs(output_path2)
    my_log.add_path(output_path + 'log.log')
    my_log.info('make dirs: {}'.format(output_path))

    first_px_path = [my_path.init_price_path_root + 'initprice_' + today_str + '.csv', my_path.init_price_path_root2 + 'initprice_' + today_str + '.csv']

    # ========================= tarding record ==========================
    trading_record_path = my_path.daily_trading_record_raw_path_root + today_str + '\\'
    trading_record_today = trading_record.get_trading_record(trading_record_path)  # [account_name, coid, trading_price trading_volume]

    # trading_record_today = trading_record_today[trading_record_today['time'].apply(lambda x: x>='12:00:00')]

    my_log.info('generating csv file: {}'.format(output_path + 'trading_record_today.csv'))
    trading_record_today.to_csv(output_path + 'trading_record_today.csv', index=False)
    trading_record_today.to_csv(output_path2 + 'trading_record_today.csv', index=False)

    first_px_df = trading_record.get_first_price(first_px_path)
    my_log.info('generating csv file: {}'.format(output_path + 'first_price.csv'))
    first_px_df.to_csv(output_path + 'first_price.csv', index=False)
    first_px_df.to_csv(output_path2 + 'first_price.csv', index=False)

    # ========================= target ==========================
    target_today = trading_target.get_target(my_path.target_path_root, today_str, traded_account_list, id_account_mapping_table)  # [coid, target, account_name]

    # ========================= stats ==========================
    trading_record_summary = stats.get_trading_summary(trading_record_today, first_px_df)
    trading_diff_summary, data_merge_all = stats.get_trading_diff_summary(trading_record_summary, target_today, account_id_mapping_table, first_px_df)
    my_log.info(trading_diff_summary)

    my_log.info('generating csv files: {}'.format(
        '\n'.join([output_path+'trading_summary.csv', output_path+'trading_detail.csv', output_path + 'data_merge_all.csv'])
    ))
    trading_diff_summary.to_csv(output_path+'trading_summary.csv', index=False, na_rep='nan')
    trading_record_summary.to_csv(output_path + 'trading_detail.csv', index=False, na_rep='nan')
    data_merge_all.to_csv(output_path + 'account_detail.csv', index=False, na_rep='nan')
    trading_diff_summary.to_csv(output_path2+'trading_summary.csv', index=False, na_rep='nan')
    trading_record_summary.to_csv(output_path2 + 'trading_detail.csv', index=False, na_rep='nan')
    data_merge_all.to_csv(output_path2 + 'account_detail.csv', index=False, na_rep='nan')

    # email_message = trading_diff_summary.to_string(index=None)
    # email_message = 'We had something wrong with Account 7 in last email. Fixed now.'
    email_message = ''
    print('please print in additional message in email:')
    add_message = input()
    my_log.info(email_message+add_message)
    mail.send_email(
        email_message+add_message,
        [output_path+'trading_summary.csv', output_path + 'account_detail.csv'],
        today_str=today.strftime('%Y-%m-%d')
    )


if __name__ == '__main__':
    main()
