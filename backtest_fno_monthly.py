import pandas as pd
import numpy as np


def get_rolling_ret(df, n):
    return df.rolling(n).apply(np.prod)


def get_top( date, ret_12, ret_6, ret_3):
    top_50 = ret_12.loc[date].nlargest(50).index
    top_30 = ret_6.loc[date, top_50].nlargest(30).index
    top_10 = ret_3.loc[date, top_30].nlargest(10).index
    return top_10


def portfolio_performance(mtl, date, ret_12, ret_6, ret_3):
    portfolio = mtl.loc[date:, get_top( date, ret_12, ret_6, ret_3)][1:2]
    return portfolio.mean(axis=1).values[0]


def run():
    df = pd.read_csv('fno_stock.csv')
    df['Date'] = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    df = df.dropna(axis=1)
    mtl = (df.pct_change() + 1)[1:].resample('M').prod()
    ret_12, ret_6, ret_3 = get_rolling_ret(mtl, 12), get_rolling_ret(mtl, 6), get_rolling_ret(mtl, 3)
    print(mtl.head())
    returns = []

    for date in mtl.index[:-1]:
        a = portfolio_performance(mtl, date, ret_12, ret_6, ret_3)
        # print(a)
        returns.append(a)
    ser = pd.Series(returns, index=mtl.index[1:])
    cum_return = ser.cumprod()
    print(ser.min())
    print(ser.max())
    print((ser[ser.apply(lambda x :x<0 )]))
    print(cum_return)


if __name__ == '__main__':
    run()
