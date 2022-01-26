import json
import requests
import pymysql
from math import ceil
import traceback

url = "http://119.3.13.193/om/cus"

# 输入接口参数
# pageNo = input("请输入分页编号")
pageSize = input("请输入分页大小")
firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
id = "e1ebbef8"
key = "8c182873"
sid = "2338"
params = {
    'id': id,
    'key': key,
    'sid': sid,
    'pageNo': 54,
    'pageSize': 10,
}

pageoutCount = 0
itemsCount = 0
# 连接数据库
db = pymysql.connect("localhost", "root", "forever1997!", "BTV")
cursor = db.cursor()
# 爬取数据


try:
    response = requests.get(url, params)
    html = json.loads(response.text)
    print("状态码：", html['resultCode'])
    print("所有数据：", html['resultData'])
    datalist = html['resultData']['dataList']
    databasic = html['resultData']['databasic']

    params = {
            'id': id,
            'key': key,
            'sid': sid,
            'pageNo': 49,
            'pageSize': pageSize,
        }
    response = requests.get(url, params)
    html = json.loads(response.text)
    datalist = html['resultData']['dataList']
    databasic = html['resultData']['databasic']



    for dict in datalist:
        print("【ID】", dict['RID'])
        print("【标题】", dict['IR_URLTITLE'])
        print("【网站名称】", dict['IR_SITENAME'])
        print("【频道名称】", dict['IR_CHANNEL'])
        print("【地址】", dict['IR_URLNAME'])
        print("【作者】", dict['IR_AUTHORS'])
        print("【发布时间】", dict['IR_URLTIME'])
        print("【摘要】", dict['IR_ABSTRACT'])
        print("【正文】", dict['IR_CONTENT'])
        print("【信息类型】", dict['SY_INFOTYPE'])
        # 存入数据库
        sql = "INSERT INTO `WHITELIST`(`ID`, `TITLE`, `CHANNEL`, `SITENAME`, `URL`, " \
              "`AUTHOR`, `TIME`, `ABSTRACT`, `CONTENT`, `INFOTYPE`) " \
              "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
              % (pymysql.escape_string(dict['RID']), pymysql.escape_string(dict['IR_URLTITLE']),
                 pymysql.escape_string(dict['IR_CHANNEL']), pymysql.escape_string(dict['IR_SITENAME']), pymysql.escape_string(dict['IR_URLNAME']),
                 pymysql.escape_string(dict['IR_AUTHORS']), pymysql.escape_string(dict['IR_URLTIME']), pymysql.escape_string(dict['IR_ABSTRACT']),
                 pymysql.escape_string(dict['IR_CONTENT']), dict['SY_INFOTYPE'])
        cursor.execute(sql)
        db.commit()
        itemsCount += 1
        print("【总条数】", databasic['allcount'])

except Exception as err:
    print(err)
    print('traceback.print_exc():', traceback.print_exc())
    print('traceback.format_exc():', traceback.format_exc())

db.close()
