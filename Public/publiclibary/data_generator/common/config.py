# -*- coding:utf-8 -*-
__author__ = 'rudolf'

#数据库连接配置

db_connects={"wallet": "mysql://root:1qaz@WSX@99.48.66.40:3306/wallet?charset=utf8", #钱包数据
             "credit": "mysql://creditlimit@mime:SIT_mime2016@99.48.58.196:3306/creditlimit?charset=utf8",#额度系统
             "coupon": "mysql://couponuser:couponuser@99.48.58.196:3306/coupon?charset=utf8",#优费券系统
             "user": "mssql+pymssql://xingwang.han:MiMe@2015@99.48.66.112:1433/memedaidb?charset=utf8", #user 数据库
            }


table_colums={"CRM.MEMBER":("MEMBER_ID","CREATE_TIME","MEMBER_TYPE","MEMBER_NAME","MOBILE_NO", "source"), #用户信息表，增加一个来源source
             "apply_info":("apply_type","member_id","cellphone","identification_name","identification_id","apply_status","created_datetime","apply_no","zx_result"), # 钱包申请表
             "money_box":("member_id","apply_no","actived_datetime","expired_date"), #钱柜表
             "money_box_order":("order_no","member_id","order_type","status","amount","repayment_periods","repayment_type",
                             "merchant_id","store_id","product_id","product_name","mobile","allies_code","merchant_industry_type","merchant_cl_type"),#订单表
             "credit_cl_credit_limit":("member_id","category_id","credit_limit","expire_date"),  #额度系统
             "coupon_CP_COUPON_CODE":("COUPON_ID","COUPON_CODE","PICK_UP_TIME","PICK_UP_CHANNEL","COUPON_NAME","STATUS","MEMBER_NAME",
                            "MEMBER_PHONE","MEMBER_ID","COUPON_TYPE","EFFECTIVE_TIME","EXPIRY_TIME","DISCOUNT","VALUE","PERIODS","RANGE_TYPE"), #优费券表
             "CRM.ID_CARD":("INPUT_NAME","INPUT_ID_NO","MEMBER_ID","NAME","ID_NO","OCR_ID_NO","KEYIN_STATUS"), # 身份证信息表
             "APPL.A_APPL":("MEMBER_ID","APPL_AMT","APPL_NO","PRODUCT","APPL_TERM","APPL_REPAY_METHOD","ALLIES_CODE","PROGRAM_CODE","APPL_TIME",
                          "CLUSTER_NO","ROLE","EXISTING_FLAG"),
              "CRM.BANK_CARD":("ID","MEMBER_ID","CARD_NO", "NAME","CARD_NO_SNAP","ISSUE_BANK_NAME","ISSUE_BANK","ISSUE_BANK_BRANCH", "CHANNEL",
               "IS_BIND_FASTPAYMENT", "CREATE_TIME","BANK_PHONE","DEFAULT_USE","CARD_TYPE","IS_VALID","CARD_BIN","CARD_LEVEL","ID_NO","PURPOSE"),
              "FSS.ACCOUNT_CASH":("ACCOUNT_NO","MEMBER_ID","MERCHANT_NO","BALANCE"),
             "CRM.MEMBER_WECHAT":("MEMBER_ID","SUBSCRIBE","OPENID","NICKNAME","SEX","LANGUAGE","HEADIMGURL","SUBSCRIBE_TIME","UNIONID","FIRST_SUBSCRIBE_TIME","LAST_UPDATE_time")
             }



sql_phone = "select count(1)  from CRM.MEMBER where MOBILE_NO ="

sql_idcard = "select count(1) from CRM.ID_CARD WHERE ID_NO="

sql_sequence = "select NEXT_VALUE  from  CRM.SEQUENCE  where SEQ_NAME='MEMBER_ID'"

merchent_sql = "select  ALLIES_NAME ,BANK_NAME ,ACCOUNT_NO,UNIONPAY_BANK_NUMBER from CRM.ALLIES where ALLIES_CODE = "


ProductInfo_sql = 'select PROGRAM_NAME,ENUM_AMT,BEGIN_AMT,END_AMT,AVAILABLE_PERIOD,AVAILABLE_REPAY_METHOD, \
                pa.APR,pf.RATE_VALUE  \
                from MKT.PROGRAM  pr  inner join CRM.ALLIES al on  pr.MERCHANT=al.ALLIES_CODE LEFT join  \
                FSS.PRICING_APR pa on pr.PROGRAM_CODE=pa.PROGRAM_CODE LEFT join  FSS.PRICING_FEE pf on pr.PROGRAM_CODE=pf.PROGRAM_CODE \
                WHERE pr.EXPIRE_TIME>GETDATE() AND pr.PROGRAM_CODE= '

REPAY_METHOD = {"554": "INSTALLMENT", "331": "AVERAGE_CAPITAL_PLUS_INTEREST"}

########## 创建贷款 dubbo 配置 ############

loans_interface_name = "cn.memedai.loan.facade.business.DubboLoanCreateBusiness"
loans_method_name = "createLoan"
parameter_types = ["cn.memedai.loan.facade.request.LoanCreateForm"]
zookerpath = "zookeeper://99.48.66.13:2181"
version = '1.0.0'


