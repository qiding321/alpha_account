# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:05

@version: python3.5
@author: qiding
"""
import socket

name = socket.gethostname()


if name == '2013-20151201LG':
    output_path_root = r'E:\MyTrading\IntradayAccount\Account\AlphaAccountDailySummary' + '\\'
    log_path = r'E:\MyTrading\IntradayAccount\Log\log.log'

    daily_trading_record_raw_path_root = r'\\SHIMING\trading\trading_summary' + '\\'
    target_path_root = r'\\SHIMING\trading\target_files' + '\\'

    no7_account_root = r'E:\MyTrading\IntradayAccount\Account\No7DailyAccount' + '\\'