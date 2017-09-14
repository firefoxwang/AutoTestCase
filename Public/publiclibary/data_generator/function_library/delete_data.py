# -*- coding:utf-8 -*-
from common.oprerate_db import *
__author__ = 'rudolf'

def __del_suersql_info(memberid, loan_id):
        # 删除用户基本信息
        sql_user = "declare @member_id int set @member_id = "+ str(memberid) +"\
                    DELETE APPL.A_APPL WHERE MEMBER_ID = @member_id  \
                    DELETE APPL.A_PRECREDIT WHERE MEMBER_ID = @member_id \
                    DELETE APPL.A_BIZ_CARD WHERE MEMBER_ID = @member_id \
                    DELETE APPL.A_CAMPUS_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.ACCT_MNG_MEMBER WHERE MEMBER_ID =  @member_id \
                    DELETE CRM.BANK_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.ID_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.BUREAU_FLAG WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER_CLUSTER WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER_IMAGE WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER_WECHAT WHERE MEMBER_ID = @member_id \
                    DELETE SECU.SECURITY_INFO WHERE MEMBER_ID = @member_id \
                    DELETE SECU.UNION_USER WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER WHERE MEMBER_ID = @member_id \
                    DELETE CRM.FRIEND_WECHAT WHERE MEMBER_ID = @member_id \
                    DELETE  CRM.CONTRACT WHERE BORROWER_ID=@member_id \
                    DELETE  FSS.LOAN_REPAY_PLAN where BORROWER_ID=@member_id \
                    DELETE  FSS.LOANS where BORROWER_ID=@member_id \
                    DELETE  FSS.LOAN_SETTLE_APPL where BORROWER_ID=@member_id \
                    DELETE FROM  fss.CRL_CTRL where MEMBER_ID=@member_id \
                    DELETE FROM  FSS.CRL_USE_LOG where MEMBER_ID=@member_id \
                    DELETE FROM  BID.TARGET WHERE  BORROWER_ID=@member_id \
                    DELETE FROM    PAY.TRANSFER WHERE MEMBER_ID=@member_id \
                    DELETE FROM  PAY.PAYMENT_ORDER WHERE MEMBER_ID=@member_id  "
        # 删除账务信息
        sql_loan = '''declare @loan_id varchar set @loan_id ='{0}'
                    DELETE  FSS.LOANS_INFO  WHERE LOAN_ID ='{0}'
                    DELETE FSS.PAYMENT_OFFSET  WHERE LOAN_ID='{0}'
                    DELETE PAY.PAYMENT_ORDER_DETAIL WHERE SKU='{0}'
                    DELETE  FSS.LOANS where LOAN_ID='{0}'
                    DELETE  FSS.LOAN_REPAY_PLAN where LOAN_ID='{0}'
                    DELETE  FSS.LOAN_SETTLE_APPL where LOAN_ID='{0}'
                    DELETE FROM  PAY.PAYMENT_ORDER WHERE MEMBER_ID={1}
                    DELETE FROM  fss.CRL_CTRL where MEMBER_ID={1}
                    DELETE  FROM BID.TARGET WHERE OBJECT_ID = '{0}'
                    DELETE  FROM FSS.INVESTMENTS where BORROWER_ID ={1}
                    DELETE  FROM  FSS.ACCOUNT_CASH_DAILY where MEMBER_ID ={1}
                    DELETE  FROM  PAY.TRANSFER where MEMBER_ID ={1}
                    DELETE  FROM  BID.RECORD WHERE OBJECT_ID ='{0}'
                    '''.format(str(loan_id),memberid)
        # 删除钱包信息

        sql_wallet = '''set @member_id={1};
        set @order_no ={0};
        Delete from apply_info where member_id={1};
        Delete from failure_count where member_id={1};
        Delete from member_type where member_id={1};
        Delete from money_box where member_id={1};
        Delete from money_box_order where member_id={1};
        Delete from patch where member_id={1};
        Delete from coupon_use_history where order_no={0};
        Delete from order_status_history where order_no={0};'''.format(str(loan_id),memberid)
#
#        sql_credit ='''
#        set @member_id={0};
#        Delete from cl_credit_limit where member_id=@member_id;
#        Delete from cl_credit_use where member_id=@member_id;
#        '''.format(str(memberid))
#
#        sql_credit ='''
#        set @member_id={0};
#        Delete from cl_credit_limit where member_id=@member_id;
#        Delete from cl_credit_use where member_id=@member_id;
#        '''.format(str(memberid))

        return sql_user, sql_loan, sql_wallet

def Delete_Data(member_id, loan_id=None, del_user=1):

    if loan_id == None:
        loan_id = '000000000'

    #del_user 是否删除user 用户信息  0 不删除 1 删除
    sql_user, sql_loan, sql_wallet = __del_suersql_info(member_id,loan_id)
    oprerate_db('user', sql_user)
    oprerate_db('user', sql_loan)
    oprerate_db('wallet', sql_wallet)



