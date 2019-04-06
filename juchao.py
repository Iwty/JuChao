# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import gevent
import requests
import jsonpath
import multiprocessing
from gevent import monkey


# monkey.patch_all()

# 下载直接存储到本地
def download_image(s, url):
    with open("./data/{}.pdf".format(s), 'wb') as f:
        text = requests.get(url)
        f.write(text.content)


def main():
    urls = 'http://www.cninfo.com.cn/new/disclosure?column=szse_latest&pageNum={}&pageSize=20'
    headers = {
        'Host': 'www.cninfo.com.cn',
        'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 实现遍历翻页
    i = 1
    urls = [urls.format(i) for i in range(1, 10)]
    for url in urls:
        # 获取当前页请求返回的数据
        response = requests.post(url, headers=headers)
        result = response.json()
        # result = json.loads(content)
        # 通过jsonpath提取公示链接信息
        secName = jsonpath.jsonpath(result, "$..secName")
        announcementTitle = jsonpath.jsonpath(result, "$..announcementTitle")
        # 拼接完整的公示链接
        adjunctUrl = ["http://static.cninfo.com.cn/" + i for i in jsonpath.jsonpath(result, "$..adjunctUrl")]
        start_time = time.time()
        # 加入线程池加快下载速度
        pl = multiprocessing.Pool(4)
        for text, url in zip(announcementTitle, adjunctUrl):
            pl.apply_async(download_image, (text, url))
            # gevent.joinall([
            #
            #     gevent.spawn(download_image, s, url)
            # ])

        pl.close()
        pl.join()

        end_time = time.time()
        duration = end_time - start_time
        print("第%d页共%d个公示，花费了%f秒" % (i, len(adjunctUrl),duration))
        i += 1


if __name__ == '__main__':
    main()
