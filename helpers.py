import pandas as pd
import numpy as np


def merge_data(price_file, fundamental_file):
    """
    Read data and perform rolling join between prices and fundamental data
    """
    prices = pd.read_csv(price_file, parse_dates=['date'])
    fund = pd.read_csv(fundamental_file, parse_dates=['date'])
    
    if "type" in prices.columns:
        prices.drop(columns='type', inplace=True)

    prices.set_index("date", inplace=True)
    fund.set_index("date", inplace=True)

    prices = prices.sort_index()
    fund = fund.sort_index()

    prices = prices['20090101':'20190101']
    fund = fund['20090101':'20190101']

    df = pd.merge_asof(prices, fund, 
                       left_index=True, 
                       right_index=True, 
                       direction='backward')
    df = df.sort_index()
    
    df['lead'] = df.close.shift(4*6)
    df['R_t1'] = df.close/df.lead - 1

    return df