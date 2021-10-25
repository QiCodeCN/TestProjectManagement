# -*- coding:utf-8 -*-
# testmanager.py

from flask import Blueprint
from dbutils.pooled_db import PooledDB
from configs import config, format

from flask import request
import pymysql.cursors
import json
from utils.emailUtil import sendEmail

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

@test_manager.route("/api/test/create",methods=['POST'])
def createReqeust():
    # 获取传递的数据，并转换成JSON
    body = request.get_data()
    body = json.loads(body)

    # 定义默认返回体
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    # 判断必填参数
    if 'appId' not in body:
        resp_failed['message'] = 'appId 提测应用不能为空'
        return resp_failed
    elif 'tester' not in body:
        resp_failed['message'] = 'tester 测试人员不能为空'
        return resp_failed
    elif 'developer' not in body:
        resp_failed['message'] = 'developer 提测人不能为空'
        return resp_failed
    elif 'title' not in body:
        resp_failed['message'] = 'title提测标题不能为空'
        return resp_failed

    # 使用连接池链接数据库
    connection = pool.connection()

    # 判断增加或是修改逻辑
    with connection:
        try:
            with connection.cursor() as cursor:
                # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
                # 其中id为自增，插入数据默认数据设置的当前时间
                sqlInsert = "INSERT INTO request (title,appId,developer,tester,CcMail,verison,`type`,scope,gitCode,wiki,`more`,`status`,createUser,updateUser) " \
                            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlInsert, (
                    body["title"], body["appId"], body["developer"], body["tester"], body["CcMail"], body["version"],
                    body['type'],
                    body["scope"], body["gitCode"], body["wiki"], body["more"], '1', body["createUser"],
                    body["updateUser"]))
                # 提交执行保存新增数据
                id = cursor.lastrowid
                connection.commit()
            if body['isEmail'] == 'true':
                # 新建成功发送Email
                if body['type'] == '1':
                    version = '功能测试'
                elif body['type'] == '2':
                    version = '性能测试'
                elif body['type'] == '3':
                    version = '安全测试'

                receivers = body["tester"].split(',') + body["developer"].split(',')
                if not body["CcMail"] is None:
                    receivers = receivers + body["CcMail"].split(',')

                subject = '【提测】' + body['title']
                reuslt = sendEmail(receivers, subject, [
                    '<strong>[提测应用]</strong>',
                    body['appName'],
                    '<strong>[提测人]</strong>',
                    body['developer'],
                    '<strong>[提测版本]</strong>',
                    body['version'],
                    '<strong>[提测类型]</strong>',
                    version,
                    '<strong>[测试内容]</strong>',
                    body['scope'],
                    '<strong>[相关文档]</strong>',
                    body['wiki'],
                    '<strong>[补充信息]</strong>',
                    body['more']
                ])

                if reuslt:
                    sendOk = 1
                else:
                    sendOk = 2

                with connection.cursor() as cursor:
                    # 更新Emai是否发送成功1-成功 2-失败
                    updateEmail = "UPDATE request SET sendEmail=%s, updateUser=%s,`updateDate`= NOW() WHERE id=%s"
                    cursor.execute(updateEmail, (sendOk, body["updateUser"], id))
                    # 提交修改邮件是否发送成功
                    connection.commit()
            else:
                print('不发送邮件！')

            return resp_success
        except Exception as err:
            resp_failed['message'] = '提测失败了:' + err
            return resp_failed


@test_manager.route("/api/test/update",methods=['POST'])
def updateReqeust():

    # 获取传递的数据，并转换成JSON
    body = request.get_data()
    body = json.loads(body)

    # 定义默认返回体
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if 'appId' not in body:
        resp_failed['message'] = 'appId 提测应用不能为空'
        return resp_failed
    elif 'tester' not in body:
        resp_failed['message'] = 'tester 测试人员不能为空'
        return resp_failed
    elif 'developer' not in body:
        resp_failed['message'] = 'developer 提测人不能为空'
        return resp_failed
    elif 'title' not in body:
        resp_failed['message'] = 'title提测标题不能为空'
        return resp_failed

    # 使用连接池链接数据库
    connection = pool.connection()

    # 如果传的值有ID，那么进行修改操作，否则为新增数据
    with connection.cursor() as cursor:
        # 拼接修改语句，由于应用名不可修改，不需要做重复校验appId
        sqlUpdate = "UPDATE request SET title=%s,appId=%s,developer=%s,tester=%s,CcMail=%s,verison=%s,`type`=%s," \
                    "scope=%s,gitCode=%s,wiki=%s,`more`=%s,updateUser=%s,`updateDate`= NOW() WHERE id=%s"
        cursor.execute(sqlUpdate, (
            body["title"], body["appId"], body["tester"], body["developer"], body['tester'], body["CcMail"],
            body["version"], body["scope"], body["gitCode"], body["wiki"], body["more"], body["updateUser"],
            body["id"]))
        # 提交执行保存更新数据
        connection.commit()

    return resp_success
