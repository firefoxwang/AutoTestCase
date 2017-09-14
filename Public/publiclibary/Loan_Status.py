# -*- coding:utf-8 -*-
import sys
import random
import time
from PublicData import *
from datetime import timedelta, date
import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DDL

def __oprerate_db (db_type, sql, env='SIT'):

    '''
    Delinfo_By_Sql 通过sql 语句删除 数据  \n
        参数 db_type :数据库链接 （user） --如需新增 请在 ReferenceData 文件下按照格式新增  \n
    sql 执行的 sql 语句 \
        使用方法 : Delinfo By Sql | user | delete from xxx where xxxx | \n
    '''

    engine = create_engine(db_connects[env][db_type], echo=False)

    return_info = None

    try:
        if 'select' in sql.lower():
            return_info = engine.execute(sql).fetchall()
        elif 'exec' in sql.lower():
            sql_new=DDL(sql)
            engine.execute(sql_new)
        else :
            sql_new=DDL(sql)
            engine.execute(sql_new)
    except Exception, e:

        print "Exception:", e

    return return_info
        
def loan(memberid, loan_id, status, is_overdue, overdue_day):
    
    print memberid, loan_id, status, is_overdue, overdue_day
    
    "is_overdue 1  未逾期 ，0逾期  ,overdue_day 逾期天数  0 是未逾期， 逾期 天数 未负数 "

    #用户确认 
    sql_qr=" EXEC FSS.USP_LOAN_USER_CONFORM    @LOAN_ID = '"+loan_id+"'"
    if status == 10:
        return None
    print sql_qr
    __oprerate_db("user", sql_qr)
    #ms.ExecNonQuery_String(sql_qr)

    __oprerate_db("user", "EXEC FSS.USP_BATCH_LOAN_PUBLISH") #发布投资广场
    if status == 20 :
        return None
    #ms.ExecNonQuery_String("EXEC FSS.USP_BATCH_LOAN_PUBLISH")
    time.sleep(1)
    
    #查询  TARGET_AMT
    sql_1="SELECT  TARGET_AMT,TARGET_ID FROM BID.TARGET where BORROWER_ID="+str(memberid)+" and OBJECT_ID='"+str(loan_id)+"'ORDER BY TARGET_ID DESC"
    #print sql_1
    pay_lsit=__oprerate_db("user", sql_1)
    
    if len(pay_lsit)<1:
        print u'BID.TARGET 未查到相关数据'
    TARGET_ID=pay_lsit[0][1]
    BID_AMT=pay_lsit[0][0]
    
    #用户255投标
    loan_sql2=" EXEC BID.USP_BID_SUBMIT 255,"+ str(TARGET_ID)+","+ str(BID_AMT) +", '', '', '' "

    #loan_sql2="EXEC BID.USP_BID_SUBMIT  @INVESTOR = 255 , @TARGET_ID ="+str(TARGET_ID) +",@BID_AMT = "+str(BID_AMT)+" ,  @IP = '' , @BID_SOURCE = '' , @CLIENT_INFO = '' "
    #print loan_sql2
    for i in range(2):
        __oprerate_db('user', loan_sql2)
    time.sleep(1)
    #满标结果处理
    loan_sql3="EXEC BID.USP_BATCH_TARGET"
    __oprerate_db('user', loan_sql3)
    if int(status) == 31:
        return None
    time.sleep(1)
    #满标交易处理
    loan_sql4="EXEC FSS.USP_BID_RESULT_BATCH_PROCESS"
    __oprerate_db('user', loan_sql4)
    if status == 40:
        return None
    time.sleep(1)
    #查看待汇款记录
    search_sql="SELECT transfer_sn,TRANSFER_AMT FROM PAY.TRANSFER WHERE  DEAL_ID IS NULL and MEMBER_ID="+str(memberid)+" ORDER BY TRANS_APPLY_TIME desc"
    search_lsit=__oprerate_db('user', search_sql)
    if len(search_lsit)<1:
        print u'PAY.TRANSFER 未查到相关数据'
    TRANSFER_SN=search_lsit[0][0]
    TRANSFER_AMT=search_lsit[0][1]
    d = datetime.datetime.now()
    
    if  is_overdue==0:
        data_str=date.today() + timedelta(days = overdue_day)
        __oprerate_db('user', "EXEC FSS.USP_SET_PARAMENT 'CURRENT_BUSINESS_DAY','"+str(data_str)+"'")
        __oprerate_db('user', "EXEC FSS.USP_SET_PARAMENT 'CURRENT_BATCH_DAY','"+str(data_str)+"'")
    #标记转账记录为“成功”
    loan_sql5="EXEC FSS.USP_TRANSFER_RESULT_UPDATE  @TRANSFER_SN ="+TRANSFER_SN+" ,  @PROCESS_RESULT = '10' ,  @RESULT_AMT =" +str(TRANSFER_AMT)+", @DEALER = 'MANUL' , @DEAL_ID ="+ \
            TRANSFER_SN+" , @DEAL_TIME = '2016-06-09 10:14:19' , @ERROR_MSG = '' "
            
    __oprerate_db('user', loan_sql5)
    if is_overdue==0:
        yester_day=date.today() + timedelta(days = -1) 
        update_fss_sql="update fss.FSS_PARAMENTS  set PARA_VALUES='"+str(yester_day)+"'  where PARA_NAME IN ('CURRENT_BATCH_DAY','CURRENT_BUSINESS_DAY')"
        __oprerate_db('user', update_fss_sql)
    
    #跑批逾期数据
    
    if is_overdue==0:
        #获取一月前当天
        #第一期逾期
        term_data_sql="SELECT PLAN_DUE_DATE  FROM FSS.LOAN_REPAY_PLAN where  BORROWER_ID="+str(memberid) +" and LOAN_ID='" +loan_id+"' order by PLAN_DUE_DATE"
        #print term_data_sql
        term_data1=__oprerate_db('user', term_data_sql)
        print term_data1
        for date_due in term_data1:
            
            if date_due[0]<str(date.today()):
                sql_overdue='''
                     DECLARE @LOAN_ID VARCHAR(32)
                     DECLARE @DATE DATE
                    SET @LOAN_ID = '{0}'
                    SET @DATE = '{1}'
                    EXEC FSS.USP_BATCH_OVERDUE_SETTLEMENT @DATE
                    EXEC FSS.USP_LOAN_CLEAR @LOAN_ID
                    EXEC FSS.USP_LOAN_DUE_DAY @LOAN_ID, @DATE
                    EXEC FSS.USP_LOAN_CAL_OVERDUE_INSTEREST @LOAN_ID, @DATE
                    EXEC FSS.USP_LOAN_CYCLE_DAY @LOAN_ID, @DATE
                    '''.format(loan_id,date_due[0])
                __oprerate_db('user', sql_overdue)
        sql_overdue='''
                     DECLARE @LOAN_ID VARCHAR(32)
                     DECLARE @DATE DATE
                    SET @LOAN_ID = '{0}'
                    SET @DATE = '{1}'
                    EXEC FSS.USP_BATCH_OVERDUE_SETTLEMENT @DATE
                    EXEC FSS.USP_LOAN_CLEAR @LOAN_ID
                    EXEC FSS.USP_LOAN_DUE_DAY @LOAN_ID, @DATE
                    EXEC FSS.USP_LOAN_CAL_OVERDUE_INSTEREST @LOAN_ID, @DATE
                    EXEC FSS.USP_LOAN_CYCLE_DAY @LOAN_ID, @DATE
                    '''.format(loan_id,str(date.today()))
        __oprerate_db('user', sql_overdue)
    return 'OK'
#if __name__=='__main__':
#    loan(816402,'2016092610000510',50, 1, 0)