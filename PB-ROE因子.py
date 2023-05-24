import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import rqdatac as rq
from rqfactor import *
from rqfactor.extension import *

plt.rcParams["font.sans-serif"] = ["SimHei"]
rq.init()
TOP(Factor('close'), threshold=50, method='ordinal')
sue = (Factor("net_profit_mrq_0") - Factor("net_profit_mrq_4"))/STD(Factor("net_profit_mrq_0") - Factor("net_profit_mrq_1"),250)
sur = (Factor("revenue_mrq_0") - Factor("revenue_mrq_4"))/STD(Factor("revenue_mrq_0") - Factor("revenue_mrq_1"),250)
growth = CS_ZSCORE(sue+sur+Factor("return_on_equity"))
d0 = "20100101"
d1 = '20130101'
d2 = '20230101'
ids=rq.index_components('000300.XSHG', '20170101')
returns=rq.get_price_change_rate(ids, start_date=d1, end_date=d2, expect_df=True)+1
#为了使用resample能更便捷聚合收益率数据，这里直接将收益率数据index平移一个交易日
returns.index=rq.get_trading_dates(rq.get_previous_trading_date(returns.index[0]), rq.get_previous_trading_date(returns.index[-1]), market='cn')
returns.columns.name=''
returns.index=pd.DatetimeIndex(returns.index)
#returns.index平移后，聚合的为当月第二个交易日到下一个月第一个交易日的收益率数据
returns=returns.resample('BM').prod()-1
returns.index=pd.DatetimeIndex(returns.index.date)
returns.columns.name=''
growth_data = execute_factor(growth,ids,d1,d2)
pb_data = execute_factor(Factor("pb_ratio"),ids,d0,d2)
def quantile_filter(df,percent,v1,v2):
    temp = df.mask((df.T-df.quantile(percent,axis=1)).T>0, v1)
    temp = temp.mask(temp!=v1,v2)
    return temp
def get_previous_month_turnover(order_book_ids, start_date, end_date, fields="month"):
    df = rq.get_turnover_rate(order_book_ids, start_date, end_date, fields=fields)
    return pd.pivot(df.reset_index(),index="tradedate",columns="order_book_id",values="month")
M_TURNOVER = UserDefinedLeafFactor("M_TURNOVER",get_previous_month_turnover)
turnover_df = execute_factor(M_TURNOVER,ids,d1,d2)
factor1 = quantile_filter(pb_data,0.4,1,0).loc[d1:]
growth_factor = quantile_filter(growth_data,0.8,1,0)
pb_factor = quantile_filter(pb_data,0.4,0,1)
factor1 = quantile_filter(pb_data,0.9,1,0).loc[d1:]
turnover_factor = quantile_filter(turnover_df,0.8,0,1)
stock_hold = growth_factor+factor1
stock_hold = stock_hold.resample("BM").last()
stock_hold = stock_hold.mask(stock_hold==0,0)
stock_hold = stock_hold.mask(stock_hold!=0,1)
stock_hold = (stock_hold.T/stock_hold.sum(axis=1)).T
ratio2 = pb_data.rolling(750).quantile(0.1)
ratio3 = pb_data.rolling(125).quantile(0.9)
ratio_factor1 = pb_data.mask(pb_data>ratio2,1)
ratio_factor1 = ratio_factor1.mask(ratio_factor1!=1,0)
ratio_factor2 = pb_data.mask(pb_data<ratio3,1)
ratio_factor2 = ratio_factor2.mask(ratio_factor2!=1,0)
ratio_factor1 = ratio_factor1.loc[d1:]
ratio_factor2 = ratio_factor2.loc[d1:]
stock_hold = growth_factor+pb_factor+ratio_factor1+ratio_factor2+turnover_factor
stock_hold = stock_hold.loc[d1:]
stock_hold = stock_hold.resample("BM").last()
stock_hold = stock_hold.mask(stock_hold==5,1)
stock_hold = stock_hold.mask(stock_hold!=1,0)
stock_hold = (stock_hold.T/stock_hold.sum(axis=1)).T
(stock_hold * returns).sum(axis=1).cumsum().plot()