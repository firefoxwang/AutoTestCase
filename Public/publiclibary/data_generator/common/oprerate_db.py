# -*- coding:utf-8 -*-
from sqlalchemy import *
import config

__author__ = 'rudolf'
# def oprerate_db(db_type, sql):
#
#     '''
#     Delinfo_By_Sql 通过sql 语句删除 数据  \n
#         参数 db_type :数据库链接 （user） --如需新增 请在 ReferenceData 文件下按照格式新增  \n
#     sql 执行的 sql 语句 \
#         使用方法 : Delinfo By Sql | user | delete from xxx where xxxx | \n
#     '''
#
#     engine = create_engine(config.db_connects[db_type], echo=False)
#
#     return_info = None
#
#     try:
#         if 'mysql' in config.db_connects[db_type]:
#             #'若有主外键约束，先取消设置，然后设置'
#             engine.execute("SET FOREIGN_KEY_CHECKS=0 ")
#             if 'select' in sql:
#                 return_info = engine.execute(sql).fetchall()
#             else:
#                 engine.execute(sql)
#             engine.execute("SET FOREIGN_KEY_CHECKS=1 ")
#         else:
#             if 'select' in sql:
#                 return_info = engine.execute(sql).fetchall()
#             else:
#                 engine.execute(sql)
#     except Exception, e:
#
#         print "Exception:", e
#
#     return return_info

def isnert_table(table_name, db_type, data_list):
    engine = create_engine(config.db_connects[db_type], echo=False)
    metadata = MetaData(engine)

    if 'mssql' in config.db_connects[db_type]:
        _schema = table_name.split(".")[0]
        table_name = table_name.split(".")[1]
    else:
        _schema = None
        table_name = table_name

    table_info = Table(table_name, metadata, autoload=True, schema=_schema)
    conn = engine.connect()
    conn.execute(table_info.insert(), data_list)


def oprerate_db(db_type, sql):

    '''
    Delinfo_By_Sql 通过sql 语句删除 数据  \n
        参数 db_type :数据库链接 （user） --如需新增 请在 ReferenceData 文件下按照格式新增  \n
    sql 执行的 sql 语句 \
        使用方法 : Delinfo By Sql | user | delete from xxx where xxxx | \n
    '''

    engine = create_engine(config.db_connects[db_type], echo=False)

    return_info = None

    try:
        if 'select' in sql.lower():
            return_info = engine.execute(sql).fetchall()
        elif 'exec' in sql.lower():
            sql_new = DDL(sql)
            engine.execute(sql_new)
        else:
            sql_new = DDL(sql)
            engine.execute(sql_new)
    except Exception, e:

        print "Exception:", e

    return return_info
