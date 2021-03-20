#场内交易
import os
import os.path
import sys
import json
import requests 

fund_list = []
fund_dict = {}

#--------------------自动爬取所有基金-----------------------
for line in  open('all_fund_code_name_type.txt'):
    code = line[0:6]
    name_type = ''
    change = 1
    fund_list.append(code)
    for s in range(8, len(line)):
        if line[s] != ' ':
            if (line[s] == '/') | (line[s] == '\\'):
                name_type = name_type + '_'
            else:
                name_type = name_type + line[s]
        else:
            if change == 1:
                tmp = {code : name_type}
                fund_dict.update(tmp)
            name_type = ''
            change = 2
#----------------------------------------------------------------

#----------------------指定你想爬取的基金-------------------------
#
#step 1:按顺序填写基金代码
#fund_list = [
#    '510710', '110003', '510310', '110020', '510580',
#    '161017', '510880', '090010', '159905', '512750',
#    '160716', '159916', '530015', '310398', '512260',
#    '513050', '159928', '001550', '512200', '161721',
#    '165525', '512800', '001552', '510900', '02800' ,
#    ]

#step 2:按顺序填写代码和名称
#fund_dict = {
#    '510710': '博时上证50ETF(场内)',
#    '110003': '易方达上证50A(场外)',
#    '510310': '易方达沪深300(场外)',
#    '110020': '易方达沪深300ETF联接A(场外)',
#    '510580': '易方达中证500指数(场内)',
#    '161017': '富国中证500指数LOF(场外)',
#    '510880': '上证红利(场内)_510880',
#    '090010': '大成中证红利指数(场外)',
#    '159905': '工银深证红利ETF(场内)',
#    '512750': '基本面50(场内)',
#    '160716': '基本面50(场外)',
#    '159916': '基本面60(场内)',
#    '530015': '基本面60(场外)',
#    '310398': '300价值(场外)',
#    '512260': '500低波动(场内)',
#    '513050': '中概互联_513050',
#    '159928': '汇添富中证主要消费ETF(场内)',
#    '001550': '医药100(场外)',
#    '512200': '南方中证全脂房地产(场内)',
#    '161721': '招商300地产等权分级(场外)',
#    '165525': '基建工程(场内)',
#    '512800': '中证银行ETF(场内)',
#    '001552': '天弘中证证券保险A(场外)',
#    '510900': 'H股ETF(场内)',
#    '02800' : '盈富基金(港股账号)',
#}
#-------------------------------------------------------------------

cookies = {
    'HAList': 'f-0-000001-^%^u4E0A^%^u8BC1^%^u6307^%^u6570',
    'em_hq_fls': 'js',
    'qgqp_b_id': 'dffc6337f5e72d5775b5a0896255f1e6',
    'st_si': '42538501481765',
    'st_asi': 'delete',
    'st_pvi': '67381059608346',
    'st_sp': '2019-10-24^%^2010^%^3A32^%^3A15',
    'st_inirUrl': 'http^%^3A^%^2F^%^2Ffund.eastmoney.com^%^2F',
    'st_sn': '6',
    'st_psi': '20210313162353792-0-5538026823',
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://fundf10.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
folder = os.getcwd() + '\\fund_data\\'
if not os.path.exists(folder):
    os.makedirs(folder)
    print(1)
print(folder)
    
for fund_code in fund_list:

    file_name = folder + str(fund_code) + '_' + fund_dict.get(fund_code) + '.data'
    result = os.path.exists(file_name)
    if result == True:
        continue

    fid = open(file_name, "w")

    fid.write('   日期     单位净值(元)    累计净值(元)  涨幅(%)\n')
    while_flag = 1
    i = 1
    while while_flag == 1:
        params = (
            #('callback', 'jQuery183039727575280775795_1615623372922'),
            ('fundCode', fund_code),
            ('pageIndex', str(i)),
            ('pageSize', '5000'),
            ('startDate', ''),
            ('endDate', ''),
            ('_', '1615624862042'),
        )


        response = requests.get('https://api.fund.eastmoney.com/f10/lsjz', headers=headers, params=params, cookies=cookies, timeout=500)
        
        # connect normally
        print(response)
        resp_dict = json.loads(response.text)
        datas     = resp_dict.get('Data')
        if datas == None:
            fid.write('can not find this fund data\n')
            break
        data      = datas.get('LSJZList')
        print('爬取基金 ' + fund_code + '_' + fund_dict.get(fund_code) + ' 的第' + str(i) + '页')

        if data:
            for d in data:
                date    = d.get('FSRQ')
                s_value = d.get('DWJZ')
                a_value = d.get('LJJZ')
                percent = d.get('JZZZL')
                if s_value == '':
                    s_value = 'none  '
                if a_value == '':
                    a_value = 'none  '
                if percent == '':
                    percent = 'none  '
                fid.write(date+ '    ' + str(s_value) + '         ' + str(a_value) + '      ' + str(percent) + '\n')
        else:
            print('completed!')
            while_flag = 0
        i = i + 1

    fid.close()

os.system('pause')
    