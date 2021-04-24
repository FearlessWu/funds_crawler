import os

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

    _day = _year * 365 + _leap_day + month_dict[(_month - 1)] + day
    _leap_flag = is_leap_year(_year)
    if _leap_flag:
        if _month < 2:
            _day = _year * 365 + _leap_day + month_dict[(_month - 1)] + day - 1
    return _day


if __name__ == '__main__':
    # step1:获取基金数据
    data_dict = {}
    flag = 1
    for line in open('fund_data\\000001_华夏成长混合.data'):
        if flag == 1:
            flag = 0
            continue

        ele_list = line.split()  # 以空格作为分割符将字符串分割

        data_ls = []
        if (len(ele_list)):
            date = ele_list[0]

            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            doy = get_day(year, month, day)
            del ele_list[0]
            data_ls.clear()
            data_ls.append(doy)
            for m in ele_list:
                if m == 'none':
                    m = 0
                data_ls.append(float(m))
            data_dict[date] = data_ls

    # step2:基金净值走势图
    os.system("pause")
