# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import requests
import json
import time


# 通过对数据的页数记录爬取
class JuchaoSpider(object):

    def __init__(self):
        self.url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=A8784B7FFB4DE75CE270DC4BD092E3E8; JSESSIONID=A8784B7FFB4DE75CE270DC4BD092E3E8; cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; _sp_ses.2141=*; _sp_id.2141=d9b9db3e-ebc5-4307-a374-064683e30af9.1553658423.31.1555925496.1555920220.92290934-eafa-49a7-ba88-c9bf76529e02",
            "Host": "www.cninfo.com.cn",
            "Origin": "http://www.cninfo.com.cn",
            "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-szse-main",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.cates = []
        with open('./category_gg.txt', 'r', encoding="utf-8") as f:
            for line in f.readlines():
                if len(line) > 1:
                    i = json.loads(line.strip())
                    self.cates.append(i)

    def start_requests(self, page, cate, d, sort):
        parsms = {
            "pageNum": page,
            "pageSize": "50",
            "tabName": "fulltext",
            "column": "sse",
            "stock": "",
            "searchkey": "",
            "secid": "",
            "plate": "sh",
            "category": cate,
            "trade": "",
            "seDate": "%s" % (d)
        }
        resp = requests.post(self.url, headers=self.headers, params=parsms)
        result = json.loads(resp.text)["totalAnnouncement"]
        page = result // 50 + 1
        self.get_data(page, cate, d, sort)

    def get_data(self, page, cate, d, sort):
        for ye in range(1, page + 1):
            parsms = {
                "pageNum": ye,
                "pageSize": "50",
                "tabName": "fulltext",
                "column": "sse",
                "stock": "",
                "searchkey": "",
                "secid": "",
                "plate": "sh",
                "category": cate,
                "trade": "",
                "seDate": "%s" % (d)
            }
            print(parsms)
            resp = requests.post(self.url, headers=self.headers, params=parsms)
            result = json.loads(resp.text)
            for dat in result["announcements"]:
                item = {}

                item['代码'] = dat['secCode']
                item['简称'] = dat['secName']

                item['公告标题'] = dat['announcementTitle']
                item['公告链接'] = 'http://static.cninfo.com.cn/' + dat['adjunctUrl']

                timeStamp = int(dat['announcementTime'])
                timeStamp /= 1000.0
                timearr = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d~%H:%M:%S", timearr)
                item['公告时间'] = otherStyleTime
                item['公告类型'] = sort
                item['爬取时间'] = time.strftime("%Y-%m-%d~%H:%M")

                self.save(item)

    def save(self, item):
        with open("./juchao_hs.json", "a", encoding="utf-8")as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def run(self):
        page = 1
        a = str(time.time()).split('.')[0]
        timearr = time.localtime(int(a) - 86400)
        d = (time.strftime("%Y-%m-%d", timearr))
        # 自动获取时间段的每一天
        # start = '2019-04-25'
        # end = '2019-06-21'
        # datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        # dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        #
        # while datestart < dateend:
        #     datestart += datetime.timedelta(days=1)
        #     per = datestart.strftime('%Y-%m-%d')
        for jc in self.cates:
            cate = jc['cate']
            sort = jc['sort']
            self.start_requests(page, cate, d, sort)


if __name__ == '__main__':
    juchao = JuchaoSpider()
    juchao.run()
