# -*- coding:utf-8 -*-
# application.py

from flask import Blueprint
from dbutils.pooled_db import PooledDB
from configs import config, format

from flask import request
import pymysql.cursors
import json

# 使用数据库连接池的方式链接数据库，提高资源利用率
pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor)

test_dashboard = Blueprint("test_dashboard", __name__)


@test_dashboard.route("/api/dashboard/stacked", methods=['POST'])
def get_request_stacked():
    # body = json.loads(request.get_data())
    connection = pool.connection()

    with connection.cursor() as cursor:
        sql_select = 'SELECT DATE_FORMAT(request.createDate,"%Y%u") weeks, apps.note, COUNT(apps.id) counts FROM request LEFT JOIN apps ON request.appId = apps.id GROUP BY weeks, apps.note;'
        cursor.execute(sql_select)
        table_data = cursor.fetchall()

    # 第一次循环过滤生成week和notes，并生成做临时关键词储备数据，
    # 用户第二次循环生成 series 需要数据
    weeks = []
    notes = []
    key_value = {}
    for row in table_data:
        week = row['weeks']
        note = row['note']
        if not week in weeks:
            weeks.append(week)
        if not note in notes:
            notes.append(note)

        key_value[week+note] = row['counts']

    # 做一个排序 小到大
    weeks.sort()

    # 做对应日期下应用数据列表生成，没有数据的week用0填充，保证顺序长度一致
    series = {}
    for note in notes:
        series[note] = []
        for week in weeks:
            if week+note in key_value:
                series[note].append(key_value[week+note])
            else:
                series[note].append(0)
    resp_data = {
        'weeks': weeks,
        'note': notes,
        'series': series
    }

    resp = format.resp_format_success
    resp['data'] = resp_data
    return resp