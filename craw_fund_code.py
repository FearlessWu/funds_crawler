import requests
import json
import os
import sys
headers = {
    'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

params = (
    ('v', '20210315224855'),
)

response = requests.get('http://fund.eastmoney.com/js/fundcode_search.js', headers=headers, params=params)

data_text = response.text[9 : (len(response.text) - 1)]

fid = open('all_fund_code_name_type.txt', 'w')
flag = 0
num = 0
for cnt in range(0, len(data_text)):
    if (data_text[cnt] == '"') & (flag != 1):
        flag = 1
        num = num + 1
        continue
    if (flag == 1) & (data_text[cnt] == '"'):
        flag = 0
        if num == 5:
            fid.write('\n')
            num = 0
        else:
            fid.write(' ')
    if flag == 1:
        if (num == 2) | (num == 5):
            continue
        fid.write(data_text[cnt])
    
print(data_text)
fid.close()
os.system('pause')