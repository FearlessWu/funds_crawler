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

def plot_history_fund(_data_list, _file_name):
    start = 1
    stop  = len(_data_list)
    x = np.linspace(start, stop, len(_data_list))
    jz = []
    ljjz = []
    date = []
    rate = []
    x_tick = []
    length = len(_data_list)
    for s in range(0, length):
        jz.insert(0, _data_list[s][2])
        ljjz.insert(0, _data_list[s][3])
        date.insert(0, _data_list[s][0])
        rate.insert(0, _data_list[s][4])

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


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
    plt.clf()
    plt.close('all')
    fig = plt.figure(figsize = (12,6))

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    (file_path, file_name_ex) = os.path.split(_file_name)
    file_name, extension = os.path.splitext(file_name_ex)
    plt.subplot(2, 2, 1)
    plt.plot(x, jz, label = '净值')
    plt.plot(x, ljjz, label = '累计净值')
    plt.xticks(x_tick, date_tick, color = 'red', rotation = '40')
    plt.ylabel('单位：元')
    plt.title(file_name)
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(x, rate, label='涨幅')
    plt.xticks(x_tick, date_tick, color='red', rotation='40')
    plt.ylabel('单位：%')
    plt.grid()
    plt.legend()
    plt.tight_layout()

    if not os.path.exists('fund_pic'):
        os.makedirs('fund_pic')
    abs_path = 'fund_pic/' + file_name + '.png'
    plt.savefig(abs_path)
    # plt.show()

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
        if 'can not find this fund data' in line:
            return data_list

        if 'none' in line:
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
                data_ls.append(float(m))
            data_list.append(data_ls)
    return data_list

def get_all_fund_file_name(_file_path, _file_list):
    # root:  当前路径
    # dirs:  子文件夹列表
    # files: 当前文件夹下的文件列表
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            file = os.path.join(root, file)
            _file_list.append(file)
        for dir in dirs:
            os.path.join(root, dir)
            get_all_fund_file_name(dir, _file_list)

if __name__ == '__main__':
    # step1:获取基金数据
    # file_name = 'fund_data/000001_华夏成长混合.data'
    file_list = []
    file_path = 'fund_data'
    get_all_fund_file_name(file_path, file_list)
    for file_name in file_list:
        viewer = 'processing ' + file_name
        print(viewer)
        data_list = get_fund_data(file_name)
        if len(data_list) != 0:
            #step2:画图
            plot_history_fund(data_list, file_name)
