# coding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import tickets, output_path, today

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 收益评价函数
# 当前价值 = 股票价值 + 现金
def pre_profit(df):
    money = 1.  # 初始金额
    last_buy = -1.  # 上次是否买入
    tickets = 0.    # 拥有股票数目
    price = 0.      # 股票现价
    for index in df.index:
        buy = df.loc[index, 'predict']
        price = df.loc[index, 'close']
        if buy != last_buy:
            money = money + tickets * price
            tickets = money * buy / price
            money = money * (1.0 - buy)
            last_buy = buy
    money = money + tickets * price
    return money

# 计算大盘正常收益
def normal_profit(df):
    begin = df.loc[df.index[0], 'close']
    end = df.loc[df.index[-1], 'close']
    return 0. + (end/begin)

# 评价函数
# predict 预测序列
# df 用于计算股票日期和股票分组
def eval(predict, df):

    predict_time_interval = predict.shape[0]
    output_size = predict.shape[1]
    predict_buy = []
    data = df.loc[:, list(tickets.keys())]
    x_date = df.loc[:, 'date'].values
    for i in range(predict.shape[0]):
        for j in range(output_size):
            if j < len(list(tickets.keys())):
                codes = tickets[data.columns[j]]
                new = [[x_date[-predict_time_interval + i], predict[i, j], code] for code in codes]
                predict_buy.extend(new)

    predict_buy_df = pd.DataFrame(predict_buy, columns=['date', 'predict', 'code'])
    predict_buy_df.sort_values(['code', 'date'], ascending=True, inplace=True)

    price_df = pd.read_csv((output_path + 'history' + '.csv'), dtype={'code': str})  # 读入股票数据
    price_df = price_df.loc[:, ['date', 'code', 'high', 'low', 'close']]

    merged_price_buy = pd.merge(predict_buy_df, price_df, 'inner', on=['code', 'date'])
    merged_price_buy.sort_values(['code', 'date'], ascending=True, inplace=True)

    # print(merged_price_buy.groupby("code").head(1))
    result_1 = merged_price_buy.groupby("code").apply(pre_profit).reset_index()
    result_2 = merged_price_buy.groupby("code").apply(normal_profit).reset_index()

    result = pd.merge(result_1, result_2, 'inner', on='code')
    result.columns = ['code', 'profit', 'normal']
    result.sort_values(['code'], ascending=True, inplace=True)

    tickets_df_list = []
    for key, val in tickets.items():
        df_temp = pd.DataFrame({'block': key, 'code': val})
        tickets_df_list.append(df_temp)
    tickets_df = pd.concat(tickets_df_list)
    tickets_df['code'] = tickets_df['code'].astype(str)

    result = pd.merge(result, tickets_df, 'inner', on='code')
    result.sort_values(['profit'], ascending=False, inplace=True)
    result.to_csv(output_path + today +'eval.csv')
    print(result)
    result = result.groupby("block")['profit', 'normal'].mean().reset_index()
    print(result)
    print(result.mean())

    plt.plot(result['block'], result['profit'], color='b', label='predict')
    plt.plot(result['block'], result['normal'], color='r', label='normal')
    plt.legend()
    plt.xticks(rotation=-90)  # 设置x轴标签旋转角度
    plt.show()


def eval_price(predict, price_df):
    merged_price_buy = pd.merge(predict, price_df, 'inner', on=['code', 'date'])
    merged_price_buy.sort_values(['code', 'date'], ascending=True, inplace=True)

    # print(merged_price_buy.groupby("code").head(1))
    result_1 = merged_price_buy.groupby("code").apply(pre_profit).reset_index()
    result_2 = merged_price_buy.groupby("code").apply(normal_profit).reset_index()

    result = pd.merge(result_1, result_2, 'inner', on='code')
    result.columns = ['code', 'profit', 'normal']
    result.sort_values(['code'], ascending=True, inplace=True)

    tickets_df_list = []
    for key, val in tickets.items():
        df_temp = pd.DataFrame({'block': key, 'code': val})
        tickets_df_list.append(df_temp)
    tickets_df = pd.concat(tickets_df_list)
    tickets_df['code'] = tickets_df['code'].astype(str)

    result = pd.merge(result, tickets_df, 'inner', on='code')
    result.sort_values(['profit'], ascending=False, inplace=True)
    result.to_csv(output_path + today +'eval.csv')
    print(result)
    result = result.groupby("block")['profit', 'normal'].mean().reset_index()
    print(result)
    print(result.mean())

    plt.plot(result['block'], result['profit'], color='b', label='predict')
    plt.plot(result['block'], result['normal'], color='r', label='normal')
    plt.legend()
    plt.xticks(rotation=-90)  # 设置x轴标签旋转角度
    plt.show()

