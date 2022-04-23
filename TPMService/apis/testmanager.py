# -*- coding:utf-8 -*-
# testmanager.py

from flask import Blueprint
from dbutils.pooled_db import PooledDB
from configs import config, format


from flask import request
import pymysql.cursors
import json
from utils.emailUtil import sendEmail

import os
from wtforms import Form,FileField
from flask import send_from_directory, make_response
from flask_wtf.file import FileRequired,FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

'''
@Author: Zhang Qi
@Copyright: 博客&公众号《大奇测试开发》
@Describe: 测试管理接口
'''

class fileForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'pdf', 'zip'])])

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
    sql_list = sql + ' ORDER BY R.updateDate DESC LIMIT {},{}'.format((currentPage - 1) * pageSize, pageSize)
    sql_count = sql + ' ORDER BY R.updateDate DESC'
    # 使用连接池链接数据库
    connection = pool.connection()

    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            count_select = 'SELECT COUNT(*) as `count` FROM request as R , apps as A ' \
                           'where R.appId = A.id AND R.isDel=0' + sql_count
            cursor.execute(count_select)
            total = cursor.fetchall()

        # 执行查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            cursor.execute('SELECT A.appId,R.* FROM request as R , apps as A '
                           'where R.appId = A.id AND R.isDel=0' + sql_list)
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
                sqlInsert = "INSERT INTO request (title,appId,developer,tester,CcMail,version,`type`,scope,gitCode,wiki,`more`,`status`,createUser,updateUser) " \
                            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlInsert, (
                    body["title"], body["appId"], body["developer"], body["tester"], body["CcMail"], body["version"],
                    body['type'],
                    body["scope"], body["gitCode"], body["wiki"], body["more"], '1', body["createUser"],
                    body["updateUser"]))
                # 提交执行保存新增数据
                id = cursor.lastrowid
                connection.commit()
            if 'isEmail' in body and body['isEmail'] == 'true':
                # 新建成功发送Email
                if body['type'] == 1:
                    rquest_type = '功能测试'
                elif body['type'] == 2:
                    rquest_type = '性能测试'
                elif body['type'] == 3:
                    rquest_type = '安全测试'

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
                    rquest_type,
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


@test_manager.route("/api/test/info", methods=['GET'])
def getTestInfo():
    test_id = request.args.get('id')

    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if not test_id:
        resp_failed.message = '提测ID不能为空'
        return resp_failed
    connection = pool.connection()
    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT A.id as appId, A.appId as appName, R.id,R.title,R.developer,R.tester,R.CcMail,R.version,R.type,R.scope,R.gitCode,R.wiki,R.more FROM request as R , apps as A where R.appId = A.id AND R.isDel=0 AND R.id={}".format(test_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            resp_success['data'] = data[0]

    return resp_success


@test_manager.route("/api/test/update", methods=['POST'])
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

    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT A.appId as appId, A.note as appName, R.id,R.title,R.developer,R.tester,R.CcMail,R.version,R.type,R.scope,R.gitCode,R.wiki,R.more FROM request as R , apps as A where R.appId = A.id AND R.isDel=0 AND R.id={}".format(
                body['id'])

            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 1:
                old_test_info = data[0]
            else:
                print('原有数据请求查询异常！')

        # 如果传的值有ID，那么进行修改操作，否则为新增数据
        with connection.cursor() as cursor:
            # 拼接修改语句，由于应用名不可修改，不需要做重复校验appId
            sqlUpdate = "UPDATE request SET title=%s,appId=%s,developer=%s,tester=%s,CcMail=%s,version=%s,`type`=%s," \
                        "scope=%s,gitCode=%s,wiki=%s,`more`=%s,updateUser=%s,`updateDate`= NOW() WHERE id=%s"
            cursor.execute(sqlUpdate, (
                body["title"], body["appId"], body["developer"], body['tester'], body["CcMail"], body["version"],
                body["type"], body["scope"], body["gitCode"], body["wiki"], body["more"], body["updateUser"],
                body["id"]))
            # 提交执行保存更新数据
            connection.commit()

            if 'isEmail' in body and body['isEmail'] == 'true':
                # 新建成功发送Email
                if body['type'] == 1:
                    rquest_type = '功能测试'
                elif body['type'] == 2:
                    rquest_type = '性能测试'
                elif body['type'] == 3:
                    rquest_type = '安全测试'

                receivers = body["tester"].split(',') + body["developer"].split(',')
                if not body["CcMail"] is None:
                    receivers = receivers + body["CcMail"].split(',')

                subject = '【提测】' + body['title']
                contents = []
                contents.append('<strong>[提测应用]</strong>')

                if old_test_info and old_test_info['appName'] != body['appName']:
                    contents.append(old_test_info['appName'] + '变更为:' + body['appName'])
                else:
                    contents.append(body['appName'])

                contents.append('<strong>[提测人]</strong>')
                if old_test_info and old_test_info['developer'] != body['developer']:
                    contents.append(old_test_info['developer'] + '变更为:' + body['developer'])
                else:
                    contents.append(body['developer'])

                contents.append('<strong>[提测版本]</strong>')
                if old_test_info and old_test_info['version'] != body['version']:
                    contents.append(old_test_info['version'] + '变更为:' + body['version'])
                else:
                    contents.append(body['developer'])

                contents.append('<strong>[测试内容]</strong>')
                if old_test_info and old_test_info['scope'] != body['scope']:
                    contents.append(old_test_info['scope'] + '变更为:' + body['scope'])
                else:
                    contents.append(body['scope'])

                contents.append('<strong>[相关文档]</strong>')
                if old_test_info and old_test_info['wiki'] != body['wiki']:
                    contents.append(old_test_info['wiki'] + '变更为:' + body['wiki'])
                else:
                    contents.append(body['wiki'])

                contents.append('<strong>[补充信息]</strong>')
                if old_test_info and old_test_info['more'] != body['more']:
                    contents.append(old_test_info['more'] + '变更为:' + body['more'])
                else:
                    contents.append(body['more'])

                reuslt = sendEmail(receivers, subject,contents)

                if reuslt:
                    sendOk = 1
                else:
                    sendOk = 2

                with connection.cursor() as cursor:
                    # 更新Emai是否发送成功1-成功 2-失败
                    updateEmail = "UPDATE request SET sendEmail=%s, updateUser=%s,`updateDate`= NOW() WHERE id=%s"
                    cursor.execute(updateEmail, (sendOk, body["updateUser"], body['id']))
                    # 提交修改邮件是否发送成功
                    connection.commit()
            else:
                print('不发送邮件！')

    return resp_success

@test_manager.route("/api/test/change", methods=['POST'])
def changeStatus():
    # 初始化返回对象
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    # 获取请求参数Body
    reqbody = json.loads(request.get_data())

    if 'id' not in reqbody:
        resp_failed['message'] = '提测ID不能为空'
        return resp_failed
    elif 'status' not in reqbody:
        resp_failed['message'] = '更改的状态不能为空'
        return resp_failed

    # 重新链接数据库
    connection = pool.connection()
    with connection.cursor() as cursor:
        # 判断状态流转的操作，如果status==start为开始测试，status==delete 软删除
        if reqbody['status'] == 'start':
            sql = "UPDATE `request` SET `status`=2 WHERE id=%s"
            resp_success['message'] = '状态流转成功，进入测试阶段。'
        elif reqbody['status'] == 'delete':
            sql = "UPDATE `request` SET `isDel`=1 WHERE id=%s"
            resp_success['message'] = '提测已被删除!'
        else:
            resp_failed.message = '状态标记错误'
            return resp_failed

        cursor.execute(sql, reqbody['id'])
        connection.commit()

    return resp_success

@test_manager.route("/api/report/upload",methods=['POST'])
def uploadFile():
    # 初始化返回对象
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    file_form = fileForm(CombinedMultiDict([request.form, request.files]))
    if file_form.validate():
        # 保存文件的相对路径
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('TPMService')[0], 'TPMService/static')
        # 获取文件
        attfile = request.files.get('file')
        file_name = secure_filename(attfile.filename)
        attfile.save(os.path.join(save_path, file_name))

        resp_success['data'] = {"fileName": file_name}
        return resp_success
    else:
        resp_failed['message'] = '文件格式不符合预期'
        return resp_failed


@test_manager.route("/api/file/download", methods=['GET'])
def downloadFile():
    fimeName = request.args.get('name')

    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('TPMService')[0], 'TPMService/static')
    response = make_response(send_from_directory(save_path, fimeName, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(fimeName)
    return response

    # 保存文件的相对路径
    # save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('TPMService')[0], 'TPMService/static')
    #
    # result = send_from_directory(save_path, fimeName, as_attachment=True)
    #
    # return result


@test_manager.route("/api/report/save", methods=['POST'])
def saveTestReport():

    # 获取传递的数据，并转换成JSON
    body = request.get_data()
    body = json.loads(body)

    # 定义默认返回体
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    # 判断必填参数
    if 'id' not in body:
        resp_failed['message'] = 'id 提测ID不能为空'
        return resp_failed
    elif 'test_desc' not in body:
        resp_failed['message'] = 'test_desc 测试结论不能为空'
        return resp_failed

    # 使用连接池链接数据库
    connection = pool.connection()

    # 方案一：根据request表中ID修改表数据添加结果
    with connection:
        try:
            with connection.cursor() as cursor:
                sqlUpdate = "UPDATE request SET status=%s,test_desc=%s,test_risks=%s,test_cases=%s,test_bugs=%s," \
                            "test_file=%s,test_note=%s,updateUser=%s,`updateDate`= NOW() WHERE id=%s"
                cursor.execute(sqlUpdate, (
                    body["status"], body["test_desc"], body["test_risks"], body['test_cases'], body["test_bugs"], body["test_file"],
                    body["test_note"], body["updateUser"], body["id"]))

                # 提交执行保存更新数据
                connection.commit()

            if 'isEmail' in body and body['isEmail'] == 'true':
                with connection.cursor() as cursor:
                    select_result = "select * from request where id={}".format(body["id"])
                    cursor.execute(select_result)
                    reports = cursor.fetchall()
                    connection.commit()

                if len(reports) == 1:
                    report = reports[0]
                    receivers = report["developer"].split(',') + report["tester"].split(',')
                    if report["CcMail"] is not None:
                        receivers = receivers + report["CcMail"].split(',')

                    subject = '【测试报告】' + report['title']
                    contents = []
                    contents.append('<strong>[测试结果]</strong>')
                    if report["status"] == 3:
                        contents.append("测试通过")
                    elif report["status"] == 4:
                        contents.append("测试失败")
                    elif report["status"] == 9:
                        contents.append("测试废弃")

                    if report['test_desc'] != "":
                        contents.append('<strong>[结论描述]</strong>')
                        contents.append(body['test_desc'])

                    if report['test_risks'] != "":
                        contents.append('<strong>[风险提示]</strong>')
                        contents.append(body['test_risks'])

                    if report['test_cases'] != "":
                        contents.append('<strong>[测试CASE]</strong>')
                        contents.append(body['test_cases'])

                    if report['test_bugs'] != "":
                        contents.append('<strong>[缺陷列表]</strong>')
                        contents.append(body['test_bugs'])

                    if report['test_note'] != "":
                        contents.append('<strong>[备 注]</strong>')
                        contents.append(body['test_note'])

                    # 附件添加
                    if report['test_file']:
                        path_file = os.path.abspath(os.path.join(os.getcwd())) + '/static/'+report['test_file']
                        attachments = [path_file]
                        reuslt = sendEmail(receivers, subject, contents, attachments)
                    else:
                        reuslt = sendEmail(receivers, subject,contents)

                    if reuslt:
                        sendOk = 1
                    else:
                        sendOk = 2

                    with connection.cursor() as cursor:
                        # 更新Emai是否发送成功1-成功 2-失败
                        updateEmail = "UPDATE request SET test_email=%s, updateUser=%s,`updateDate`= NOW() WHERE id=%s"
                        cursor.execute(updateEmail, (sendOk, body["updateUser"], body['id']))
                        # 提交修改邮件是否发送成功
                        connection.commit()
                else:
                    resp_failed['message'] = '测试报告保存成功，但邮件服务发送异常！'
                    return resp_failed
            else:
                pass

            return resp_success
        except Exception as err:
            resp_failed['message'] = '提测失败了:' + err
            return resp_failed

@test_manager.route("/api/report/info", methods=['GET'])
def getTestReoprt():
    report_id = request.args.get('id')

    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if not report_id:
        resp_failed.message = '提测 id 不能为空'
        return resp_failed
    connection = pool.connection()
    with connection.cursor() as cursor:
        # 查询提测信息表，返回报告所需要的字段值
        sql = "SELECT id,status,test_desc,test_risks,test_cases,test_bugs,test_file,test_note,test_email FROM request WHERE id={}".format(report_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            resp_success['data'] = data[0]

    return resp_success