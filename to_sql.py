# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()

text_list = [
    'juchao_hs.json',
    'juchao_dy.json'
]
# 读入数据
for text in text_list:
    data_str = open(text, encoding="utf-8").read()
    # 写入数据库
    df = pd.read_json(data_str, orient='records', lines=True, dtype=False)
    if text == 'juchao_hs.json':
        database = 'jc_master_gg'
    else:
        database = 'jc_master_dy'

    yconnect = create_engine(
        'mysql+mysqldb://fdmtdb:Fdmt1234!@rm-8vb5ggud8sugd77vc.mysql.zhangbei.rds.aliyuncs.com:3306/fdmt_dataset?charset=utf8')

    df.to_sql(name=database, con=yconnect, if_exists='append', index=False)
