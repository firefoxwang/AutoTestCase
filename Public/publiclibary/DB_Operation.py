# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import traceback

from DubboLibary import *

from Loan_Status import *
import RF_ENV
from Table_Structure import *

try:
    from pymongo import MongoClient
except ImportError as e:
    print "Exception:", e

__author__ = 'Rudolf'

def DeUplinfo_By_NoSQL (db_type, nosql):
    '''
    DeUplinfo_By_NoSQL 通过mongodb语句查询、删除 数据  \n
        参数 db_type :数据库链接 （spider） --如需新增 请在 PublicData.py 文件下按照格式新增nosql_connects字典  \n
        查询一条数据使用方法 : \n
        ${result} | Delinfo By NoSql | spider | test.phone_verify_counts.find_one({'phone': '13566007825'}) | \n
        删除一条数据使用方法 : \n
        Delinfo By NoSql | spider | test.phone_verify_counts.remove({'phone': '18802763682'}) | \n
    '''
    nosql = nosql.lower()
    print nosql

    try:
        db = nosql.split(".",2)[0]
        collection = nosql.split(".",2)[1]
        action = nosql.split(".",2)[2]
        method = action[:action.find('(')]
        k_v = eval(action[action.find('(')+1:action.find(')')])
    except Exception as err:
        print '\n'.join([str(err), traceback.format_exc()])
        k_v = None

    uri = nosql_connects[db_type]
    return_info = None

    #建立mongodb连接
    client = MongoClient(uri)

    try:
        db = client[db]
        #删除记录
        if 'remove' in method:
            #防止删除所有记录
            if not k_v in [None,'',{}]:
                db[collection].remove(k_v)
        #查询一条记录
        elif 'find_one' in method:
            return_info = db[collection].find_one(k_v)
        #查询多条记录
        elif 'find' in method:
            return_info = []
            for doc in db[collection].find(k_v):
                return_info.append(doc)
        else:
            print "不支持该mongodb命令"
    except Exception as err:
        print '\n'.join([str(err), traceback.format_exc()])
    finally:
        client.close()
        return return_info

def DeUplinfo_By_Sql (db_type, sql, env='sit'):

    '''
    Delinfo_By_Sql 通过sql 语句删除 数据  \n
        参数 db_type :数据库链接 （user） --如需新增 请在 ReferenceData 文件下按照格式新增  \n
    sql 执行的 sql 语句 \
        使用方法 : Delinfo By Sql | user | delete from xxx where xxxx | \n
    '''

    try:
        if env.lower() == 'aliuat' or RF_ENV.get_env() == 'aliuat':
            print '已选择ALIUAT数据库'
            db_info = db_connects['ALIUAT'][db_type]
        else:
            print '已选择SIT数据库'
            db_info = db_connects['SIT'][db_type]
    except Exception as err:
        print('当前数据库环境为【{0}】, 请检查Public\publiclibary\PublicData.py下是否配置【{1}】数据库'.format(env, db_type))
        print '\n'.join([str(err), traceback.format_exc()])


    engine = create_engine(db_info, echo=False)
    print engine
    return_info = None

    # 临时规避首次连接数据丢失连问题

    try:
        if 'mysql' in db_info:
            #'若有主外键约束，先取消设置，然后设置'
            if 'select' in sql.lower():
                print sql
                return_info = engine.execute(sql).fetchall()
                print return_info
            elif 'exec' in sql.lower():
                sql_new = DDL(sql)
                print sql_new
                engine.execute(sql_new)
            else:
                engine.execute(sql)
                #engine.execute("SET FOREIGN_KEY_CHECKS=1 ")
        else:
            if 'select' in sql.lower():
                return_info = engine.execute(sql).fetchall()
            elif 'exec' in sql.lower():
                sql_new = DDL(sql)
                engine.execute(sql_new)
            else:
                engine.execute(sql)
    except Exception, e:

        print "Exception:", e

    return return_info

def Isnert_Tables(table_names, *args):
    '''
    :param table_names:
    :param args:
    :return:
    '''

    if isinstance(table_names, (str, unicode)) :
        table_names = table_names.split(",")
    elif isinstance(table_names, list):
        table_names=table_names
    else:
        print '传入参数格式有误，格式为 [表名1，表名2]'
        sys.exit()

    if len(args) == 2 and args[1].upper() == 'ALIUAT':
        env = 'ALIUAT'
    else:
        env = 'SIT'

    if isinstance(args[0], list):
        args = tuple(args[0])

    TS = Table_Structure(env)
    TS.data_info(table_names, args)
    for table_name_ in table_names:
        data_list = []
        db_connect = db_connects[env][table_name_.split("_", 1)[0]]  # 数据库配置

        engine = create_engine(db_connect, echo=False)  # 数据库连接
        metadata = MetaData(engine)
        print table_name_
        if 'mssql' in db_connect:
            _schema = table_name_.split("_",1)[1].split('.',1)[0]
            table_name = table_name_.split("_",1)[1].split('.',1)[1]
        else:
            _schema=None
            table_name = table_name_.split("_",1)[1]
        table_info = Table(table_name, metadata, autoload=True,schema=_schema)
        conn = engine.connect()
        print  dict(zip(table_colums[table_name_],eval('TS.'+table_name.upper()+"_INFO") ))
        conn.execute(table_info.insert(), dict(zip(table_colums[table_name_],eval('TS.'+table_name.upper()+"_INFO") )))
        conn.close()
    return TS
def __create_loans(loans_args):
    DL=DubboLibary()
    DL.connect_to_dubbo_register(zookerpath)
    #print loans_interface_name, loans_method_name, parameter_types
    aa=DL.call_dubbo_interface_method(loans_interface_name, loans_method_name, parameter_types,version,str(loans_args))
def Create_Loan(CouponInfo={"couponIsUsed":"false"}, MerchentInfo={"allicecode":'FUKANGYIYUAN'}, ProductInfo={"PROGRAM_CODE":"c_720_FUKANGYIYUAN_3"}, loan_status=50, is_overdue=1, overdue_day=0):
    "is_overdue 1  未逾期 ，0逾期  ,overdue_day 逾期天数  0 是未逾期， 逾期 天数 未负数 "
    #创建用户信息

    if isinstance(CouponInfo, (str,unicode)) and "{" in CouponInfo and '}' in CouponInfo:
        CouponInfo_ = eval(CouponInfo)
    elif isinstance(CouponInfo, (dict)):
        CouponInfo_ = CouponInfo
    else:
        print 'CouponInfo格式错误！！！'
        sys.exit()

    if isinstance(ProductInfo, (str,unicode)) and "{" in ProductInfo and '}' in ProductInfo:
        ProductInfo_ = eval(ProductInfo)
    elif isinstance(ProductInfo, dict):
        ProductInfo_ = ProductInfo
    else:
        print 'ProductInfo格式错误！！！'
        sys.exit()

    if isinstance(MerchentInfo, (str,unicode)) and "{" in MerchentInfo and '}' in MerchentInfo:
        MerchentInfo_ = eval(MerchentInfo)
    elif isinstance(MerchentInfo, dict):
        MerchentInfo_ = MerchentInfo
    else:
        print 'MerchentInfo格式错误！！！'
        sys.exit()


    TS = Table_Structure()
    TS.loans_data(CouponInfo_, MerchentInfo_, ProductInfo_)
#    engine = create_engine(db_connects['user'], echo=False)
#    metadata = MetaData(engine)
#    table_name_="user_CRM.MEMBER"
#    _schema = table_name_.split("_",1)[1].split('.',1)[0]
#    table_name = table_name_.split("_",1)[1].split('.',1)[1]
#    table_info = Table(table_name, metadata, autoload=True,schema=_schema)
#    conn = engine.connect()
#    conn.execute(table_info.insert(), dict(zip(table_colums[table_name_],eval('TS.'+table_name.upper()+"_INFO") )))
#    conn.close()
    try:
        print TS.loans_args
        __create_loans(TS.loans_args)
    except Exception,e:
        print "创建贷款失败，Exception :",e
        sys.exit()

    if 'memberId' in ProductInfo:
        memberId=str(ProductInfo_['memberId'])
    else:
        memberId=str(TS.MEMBER_ID)
    if 'applNo' in ProductInfo:
        apply_no=str(ProductInfo_['applNo'])
    else:
        apply_no=str(TS.apply_no)


    loan(memberId, apply_no, int(loan_status), is_overdue, overdue_day)

    return TS


if __name__ == "__main__":#DELETE FROM wallet.money_box_order WHERE mobile ='13701456038';
    #DELETE FROM wallet.money_box WHERE member_id = '815946';
    a = DeUplinfo_By_Sql('wallet', "DELETE FROM money_box WHERE member_id = '820508';")
    print a
