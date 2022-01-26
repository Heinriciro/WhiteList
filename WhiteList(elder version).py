import json
import requests
import pymysql
import time
import sys
from math import ceil
import traceback


def news(url, init_params, sdate=None, edate=None):
    getpages = 0
    itemscount = 0
    pagesize = 10
    pages = 0
    try:
        response = requests.get(url, init_params)
        html = json.loads(response.text)
        print("状态码：", html['resultCode'])
        print("所有数据：", html['resultData'])
        datalist = html['resultData']['dataList']
        databasic = html['resultData']['databasic']
        count = databasic['allcount']
        print("【总条数】", databasic['allcount'])
        pages = ceil(count/int(pagesize))
        time.sleep(5)
        for i in range(1, pages):
            try:
                if sdate is None and edate is None:
                    params = {
                        'id': id,
                        'key': key,
                        'sid': sid,
                        'pageNo': i,
                        'pageSize': 10
                    }
                elif edate is None:
                    params = {
                        'id': id,
                        'key': key,
                        'sid': sid,
                        'pageNo': i,
                        'pageSize': 10,
                        'startDate': sdate
                    }
                elif sdate is None:
                    params = {
                        'id': id,
                        'key': key,
                        'sid': sid,
                        'pageNo': i,
                        'pageSize': 10,
                        'endDate': edate
                    }
                else:
                    params = {
                        'id': id,
                        'key': key,
                        'sid': sid,
                        'pageNo': i,
                        'pageSize': 10,
                        'startDate': sdate,
                        'endDate': edate
                    }
                response = requests.get(url, params)
                html = json.loads(response.text)
                datalist = html['resultData']['dataList']
                databasic = html['resultData']['databasic']
                print("【总条数】", databasic['allcount'])
                print("当前页数:", i)
                getpages += 1

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
                    itemscount += 1
                    # 存入数据库
                    sql = "INSERT INTO `WHITELIST`(`ID`, `TITLE`, `CHANNEL`, `SITENAME`, `URL`, " \
                          "`AUTHOR`, `TIME`, `ABSTRACT`, `CONTENT`, `INFOTYPE`) " \
                          "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " \
                          "ON DUPLICATE KEY UPDATE `ID`='%s';" \
                          % (pymysql.escape_string(dict['RID']), pymysql.escape_string(dict['IR_URLTITLE']),
                             pymysql.escape_string(dict['IR_CHANNEL']), pymysql.escape_string(dict['IR_SITENAME']), pymysql.escape_string(dict['IR_URLNAME']),
                             pymysql.escape_string(dict['IR_AUTHORS']), pymysql.escape_string(dict['IR_URLTIME']), pymysql.escape_string(dict['IR_ABSTRACT']),
                             pymysql.escape_string(dict['IR_CONTENT']), dict['SY_INFOTYPE'], pymysql.escape_string(dict['RID']))
                    cursor.execute(sql)
                    db.commit()

            except Exception as err0:
                print(err0)
                pass
            print("该页读取完毕")
            time.sleep(6)
            continue
    except Exception as err1:
        print(err1)
        print('traceback.print_exc():', traceback.print_exc())
        print('traceback.format_exc():', traceback.format_exc())
    print("已查询页数：", getpages)
    print("总页数：", pages)
    print("页码序列", range(1, pages))
    print("已获取条数", itemscount)


if __name__ == "__main__":
    url = "http://119.3.13.193/om/cus"
    firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    id = "e1ebbef8"
    key = "8c182873"
    sid = "2338"
    init_params = {
        'id': id,
        'key': key,
        'sid': sid,
        'pageNo': 1,
        'pageSize': 10,
    }

    while True:
        # 连接数据库
        db = pymysql.connect("localhost", "root", "forever1997!", "shujucaiji")
        cursor = db.cursor()
        # 爬取数据
        news(url, init_params)
        time.sleep(60*60*2)
        db.close()
