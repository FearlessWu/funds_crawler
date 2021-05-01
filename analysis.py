import os
from matplotlib import pylab as plt
import numpy as np

month_dict = {
    0: 0,
    1: 31,
    2: 59,
    3: 90,
    4: 120,
    5: 151,
    6: 181,
    7: 212,
    8: 243,
    9: 273,
    10: 304,
    11: 334,
    12: 365
}

def plot_history_fund(_data_list):
    start = 1
    stop  = len(_data_list)
    x = np.linspace(start, stop, len(_data_list))
    jz = []
    ljjz = []
    date = []
    x_tick = []
    length = len(_data_list)
    for s in range(0, length):
        jz.insert(0, _data_list[s][2])
        ljjz.insert(0, _data_list[s][3])
        date.insert(0, _data_list[s][0])
    fig = plt.figure(figsize = (6,6))

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.plot(x, jz, label = '净值')
    plt.plot(x, ljjz, label = '累计净值')

    # xticks设置
    grep = 9
    date_tick = []
    step = int(len(_data_list) / grep)
    date_tick.insert(0, _data_list[0][0])
    x_tick.append(1)
    for i in range(1, grep):
        date_tick.insert(0, _data_list[i * step][0])
        x_tick.append((i * step + 1))
    date_tick.insert(0, _data_list[length - 1][0])
    x_tick.append(length)

    plt.xticks(x_tick, date_tick, color = 'red', rotation = '40')
    plt.xlabel('日期')
    plt.ylabel('单位：元')
    plt.title('基金走势')
    plt.grid()
    plt.legend()
    plt.show()

# 判断是否是闰年
def is_leap_year(_year):
    if ((_year % 4 == 0) & (_year % 100 != 0)) | (_year % 400 == 0):
        return True
    else:
        return False

def get_day(_year, _month, _day):
    _leap_day = 0
    for i in range(0, _year):
        _leap_flag = is_leap_year(i)
        if _leap_flag:
            _leap_day = _leap_day + 1

    day = (_year - 1) * 365 + _leap_day + month_dict[(_month - 1)] + _day
    _leap_flag = is_leap_year(_year)
    if _leap_flag:
        if _month < 2:
            day = _year * 365 + _leap_day + month_dict[(_month - 1)] + _day - 1
    return day

def get_fund_data(_file_name):
    data_list = []
    flag = 1
    for line in open(_file_name):
        if flag == 1:
            flag = 0
            continue
        ele_list = line.split()  # 以空格作为分割符将字符串分割
        data_ls = []
        if (len(ele_list)):
            date = ele_list[0]
            year = int(date[0:4])
            month = int(date[5:7])
            day   = int(date[8:10])
            doy = get_day(year, month, day)
            del ele_list[0]
            data_ls.clear()
            data_ls.append(date)
            data_ls.append(doy)
            for m in ele_list:
                if m == 'none':
                    m = 0
                data_ls.append(float(m))
            data_list.append(data_ls)
    return data_list

if __name__ == '__main__':
    # step1:获取基金数据
    # file_name = 'fund_data/000001_华夏成长混合.data'
    file_name = 'fund_data/000008_嘉实中证500ETF联接A.data'
    data_list = get_fund_data(file_name)

    #step2:画图
    plot_history_fund(data_list)
