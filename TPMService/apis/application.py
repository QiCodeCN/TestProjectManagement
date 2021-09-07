# -*- coding:utf-8 -*-

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

app_application = Blueprint("app_application", __name__)

@app_application.route("/api/application/search",methods=['POST'])
def searchBykey():
    body = request.get_data()
    body = json.loads(body)

    # 基础语句定义
    sql = ""

    # 获取pageSize和
    pageSize = 10 if body['pageSize'] is None else body['pageSize']
    currentPage = 1 if body['currentPage'] is None else body['currentPage']


    # 拼接查询条件
    if 'productId' in body and body['productId'] != '':
        sql = sql + " AND `productId` = '{}'".format(body['productId'])
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND `appId` LIKE '%{}%'".format(body['appId'])
    if 'note' in body and body['note'] != '':
        sql = sql + " AND `note` LIKE '%{}%'".format(body['note'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND `tester` LIKE '%{}%'".format(body['tester'])
    if 'developer' in body and body['developer'] != '':
        sql = sql + " AND `developer` LIKE '%{}%'".format(body['developer'])
    if 'producer' in body and body['producer'] != '':
        sql = sql + " AND `producer` LIKE '%{}%'".format(body['producer'])

    # 排序和页数拼接
    sql = sql +' ORDER BY `updateDate` DESC LIMIT {},{}'.format((currentPage-1)*pageSize, pageSize)
    print(sql)

    # 使用连接池链接数据库
    connection = pool.connection()

    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) as `count` FROM `apps` WHERE `status`=0' + sql)
            total = cursor.fetchall()

        # 执行查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            cursor.execute('SELECT * FROM `apps` WHERE `status`=0' + sql)
            data = cursor.fetchall()

    # 按分页模版返回查询数据
    response = format.resp_format_success
    response['data'] = data
    response['total'] = total[0]['count']
    return response

@app_application.route("/api/application/product",methods=['GET'])
def getProduct():
    # 使用连接池链接数据库
    connection = pool.connection()

    with connection.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT id,keyCode,title FROM `products` WHERE `status`=0 ORDER BY `update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    # 按返回模版格式进行json结果返回
    response = format.resp_format_success
    response['data'] = data
    return response

    return response