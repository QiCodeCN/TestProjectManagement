# -*- coding:utf-8 -*-
# testmanager.py

from flask import Blueprint
from dbutils.pooled_db import PooledDB
from configs import config, format

from flask import request
import pymysql.cursors
import json

# 使用数据库连接池的方式链接数据库，提高资源利用率
pool = PooledDB(pymysql, mincached=2, maxcached=5,host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd= config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor)

test_manager = Blueprint("test_manager", __name__)

@test_manager.route("/api/test/search",methods=['POST'])
def searchBykey():
    body = request.get_data()
    body = json.loads(body)

    # 基础语句定义
    sql = ""

    # 获取pageSize和
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']

    # 拼接查询条件
    if 'productId' in body and body['productId'] != '':
        sql = sql + " AND A.productId LIKE '%{}%'".format(body['productId'])
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND A.appId LIKE '%{}%'".format(body['appId'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND R.tester LIKE '%{}%'".format(body['tester'])
    if 'developer' in body and body['developer'] != '':
        sql = sql + " AND R.developer LIKE '%{}%'".format(body['developer'])
    if 'status' in body and body['status'] != '':
        sql = sql + " AND R.status = '{}'".format(body['status'])
    if 'pickTime' in body and body['pickTime'] != '':
        sql = sql + " AND R.updateDate >= '{}' and R.updateDate <= '{}' ".format(body['pickTime'][0],body['pickTime'][1])

    # 排序和页数拼接
    sql = sql + ' ORDER BY R.updateDate DESC LIMIT {},{}'.format((currentPage - 1) * pageSize, pageSize)
    print(sql)

    # 使用连接池链接数据库
    connection = pool.connection()

    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            count_select = 'SELECT COUNT(*) as `count` FROM request as R , apps as A where R.appId = A.id AND R.isDel=0' + sql
            print(count_select)
            cursor.execute(count_select)
            total = cursor.fetchall()

        # 执行查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            cursor.execute('SELECT A.appId,R.* FROM request as R , apps as A where R.appId = A.id AND R.isDel=0' + sql)
            data = cursor.fetchall()

    # 按分页模版返回查询数据
    response = format.resp_format_success
    response['data'] = data
    response['total'] = total[0]['count']
    return response