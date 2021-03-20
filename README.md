## 环境
1、确保json库、requests库可以正常导入
## craw_fund_code.py
该文件会将爬取到的基金代码以及名称输出到当前目录中，文件名为all_fund_code_name_type.txt
## fund_data_crawler.py
1、该文件会读取all_fund_code_name_type.txt，然后依次对每个基金进行爬取。基金路径为本目录下的fund_data文件夹中。
2、由于爬取的基金数量众多，由于网络连接的原因，往往中间会报错超时错误，这里笔者也没有很好的解决，需要手动retrigger一下脚本。