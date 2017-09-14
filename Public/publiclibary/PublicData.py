# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import sys

# 数据库连接配置
redis_config = {"UAT": {"host": "r-bp1ae6d5d9d69954.redis.rds.aliyuncs.com", "port": "6379", "password": "45werWERf"},
                "SIT": {"host": "99.48.66.13", "port": "6379", "password": "1qaz@WSX"}
                }

nosql_connects = {
    "spider": "mongodb://test:test@99.48.58.22/test"  # 爬虫系统
}

# db_connects={"SIT":{ # sit数据库
#                     "wallet": "mysql+pymysql://xingwang.han:WUyan@0812@99.48.66.40:3306/wallet?charset=utf8", #钱包数据
#                     "credit": "mysql+pymysql://creditlimit@mime:SIT_mime2016@99.48.58.196:3306/creditlimit?charset=utf8",#额度系统
#                     "coupon": "mysql+pymysql://couponuser:couponuser@99.48.58.196:3306/coupon?charset=utf8",#优惠券系统
#                     "user": "mssql+pymssql://xingya.wu:Xingya@123@99.48.66.112:1433/memedaidb?charset=utf8", #user 数据库
#                     "exec_proc": "99.48.66.112,xingwang.han,MiMe@2015,memedaidb",
#                     "wallet_uat": "mysql+pymysql://xingwang.han:WUyan@0812@99.48.66.40:3306/wallet_uat?charset=utf8",  # 钱包系统 uat环境
#                     "credit_uat": "mysql+pymysql://creditlimit@mime:UAT_mime2016@99.48.58.194:3306/creditlimit?charset=utf8",  # 额度系统 uat
#                     "user_uat": "mssql+pymssql://daoqing.zha:mime@123@99.48.66.12:1433/memedaidb?charset=utf8",  # user 数据库 uat
#                     "wallet_sdk": "mysql+pymysql://wallet_sdk@mime:SIT_mime2016@99.48.58.196:3306/wallet_sdk?charset=utf8",  # wallet_sdk
#                     "wallet_sdk_uat": "mysql+pymysql://wallet_sdk@mime:UAT_mime2016@99.48.58.194:3306/wallet_sdk?charset=utf8",  # wallet_sdk uat
#                     "activity": "mysql+pymysql://activity:activity@99.48.58.196:3306/activity?charset=utf8", # 活动
#                     "notification": "mysql+pymysql://xingwang.han:WUyan@0812@99.48.66.40:3306/me_notification?charset=utf8", #me_notification
#                     "authdb": "mysql+pymysql://auth@mime:SIT_mime2016@99.48.58.196:3306/authdb?charset=utf8",#授权系统
#                     "merchant": "mssql+pymssql://liuxun:sp_admin@99.48.66.112:1433/MERCHANTAUDIT?charset=utf8", #merchant 数据库
#                     "credit-audit-core": "mysql+pymysql://creditaudit@mime:SIT_mime2016@99.48.58.196/CREDIT_AUDIT?charset=utf8",  # credit-audit-core"
#                     "opencode_sit": "mysql+pymysql://xingwang.han:WUyan@0812@99.48.66.40:3306/opencode_sit?charset=utf8", # opencode_sit
#                     "antifraud": "mysql+pymysql://antifraud@mime:SIT_mime2016@99.48.58.196:3306/antifraud?charset=utf8",#反欺诈
#                     "credit-trade-audit":"mysql+pymysql://creditta@mime:SIT_mime2016@99.48.58.196/CREDIT_TRADE_AUDIT?charset=utf8", # credit-trade-audit-core"
#         			"merchantservice":"mysql+pymysql://merchant@mime:SIT_mime2016@99.48.58.196:3306/merchantservice?charset=utf8",  #merchantservice
#                     "cashloan": "mysql+pymysql://cashloan@mime:SIT_mime2016@99.48.58.196:3306/cashloan?charset=utf8",# 现金贷

#                     },
#              "ALIUAT":{ # aliuat数据库
#                     "test_sqlserver": "mssql+pymssql://username:password@192.168.10.7:1433/database?charset=utf8", #这是一个sql-server db 配置模板
#                     "test_mysql": "mysql+pymysql://username:password@192.168.10.2:3306/database?charset=utf8", #这是一个mysql db 配置模板

#                     }
#              }

db_connects = {"SIT": {  # sit数据库
    "wallet": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.66.40:3306/wallet?charset=utf8",  # 钱包数据
    "user": "mssql+pymssql://autotestsit:Autotestsit@123@rm-bp16f7vuq5aqxf55b.sqlserver.rds.aliyuncs.com:3433/memedaidb?charset=utf8",  # user数据库
    "credit": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/creditlimit?charset=utf8",  # 额度系统
    "coupon": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/coupon?charset=utf8",  # 优惠券系统
    "exec_proc": "99.48.66.112,autotestsit,Autotestsit@123,memedaidb",
    "wallet_sdk": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/wallet_sdk?charset=utf8",  # wallet_sdk
    "activity": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/activity?charset=utf8",  # 活动
    "notification": "mysql+pymysql://autotestsit:Autotestsit@123@0812@99.48.66.40:3306/me_notification?charset=utf8",
    # me_notification
    "authdb": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/authdb?charset=utf8",
    # 授权系统
    "merchant": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.66.40:3306/merchant_audit?charset=utf8",  # merchant 数据库
    "BDS_DATA":"mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40:3306/BDS_DATA?charset=utf8",  #BDS
    "credit-audit-core": "mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40/CREDIT_AUDIT?charset=utf8",

    # credit-audit-core
    "opencode_sit": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.66.40:3306/opencode_sit?charset=utf8",  # 发码验码
    "antifraud": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/antifraud?charset=utf8",  # 反欺诈
    "credit-trade-audit": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196/CREDIT_TRADE_AUDIT?charset=utf8",
# credit-trade-audit-core
    "merchantservice": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/merchantservice?charset=utf8",
# merchantservice
    "cashloan": "mysql+pymysql://autotestsit:Autotestsit@123@99.48.66.40:3306/cashloan?charset=utf8",  # 现金贷
    "loan_new": "mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40:3306/accounting?charset=utf8",  # loan_new 数据库
    "capital": "mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40:3306/capital?charset=utf8",  # capital 数据库
    "cms_test":"mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40:3306/cms_test?charset=utf8", # cms 数据库
    "collections_mysql":"mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/collections?charset=utf8",#导购
    "merchandisecenter_mysql":"mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/merchandisecenter?charset=utf8",#商品中心
    "activity_platform":"mysql+pymysql://autotestsit:Autotestsit@123@99.48.58.196:3306/activity_platform?charset=utf8",##营销平台
    "repayment_core": "mysql+pymysql://application_sit:5tgb^YHN@99.48.66.40:3306/repayment?charset=utf8",  # loan_new 数据库
    # "loan_new": "mysql+pymysql://xiangyu.huang:Hxy@901126@99.48.66.40:3306/ACCOUNTING?charset=utf8", #loan_new 数据库
    # "loan_new": "mssql+pymssql://xiangyu.huang:1qaz@WSX@115.29.241.236:1433/memedaifss?charset=utf8", #loan_new 数据库
    # "loan_new": "mssql+pymssql://jun.li:1qaz@WSX@115.29.241.236:1433/memedaifss?charset=utf8", #loan_new 数据库
},
    "ALIUAT": {  # aliuat数据库
        "wallet": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/wallet?charset=utf8",  # 钱包系统
        "user": "mssql+pymssql://autotestuat:Autotestuat@123@192.168.10.7:1433/memedaidb?charset=utf8",  # user数据库
        "credit": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/creditlimit?charset=utf8",  # 额度系统
        "coupon": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/coupon?charset=utf8",  # 优惠券系统
        "exec_proc": "192.168.10.7,autotestuat,Autotestuat@123,memedaidb",
        "wallet_sdk": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/wallet_sdk?charset=utf8",  # wallet_sdk
        "activity": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/activity?charset=utf8",  # 活动
        "notification": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/me_notification?charset=utf8",
        # me_notification
        "authdb": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/authdb?charset=utf8",  # 授权系统
        "merchant": "mssql+pymssql://autotestuat:Autotestuat@123@192.168.10.7:1433/merchant_audit?charset=utf8",
        # merchant 数据库
        "credit-audit-core": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2/CREDIT_AUDIT?charset=utf8",
        # credit-audit-core
        "opencode_sit": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/opencode?charset=utf8",  # 发码验码
        "antifraud": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/antifraud?charset=utf8",  # 反欺诈
        "credit-trade-audit": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2/CREDIT_TRADE_AUDIT?charset=utf8",
        # credit-trade-audit-core
        "merchantservice": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/merchantservice?charset=utf8",
        # merchantservice
        "cashloan": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/cashloan?charset=utf8",  # 现金贷
        "accounting": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/cashloan?charset=utf8",  # 账务
		"loan_new": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/accounting?charset=utf8", #loan_new 数据库
        "capital": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/capital?charset=utf8",#资金方数据库
         "sdk": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/sdk?charset=utf8",  # sdk
        "collections_mysql":"mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/collections?charset=utf8",#导购
        "merchandisecenter_mysql": "mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/merchandisecenter?charset=utf8",#商品中心
		"activity_platform":"mysql+pymysql://autotestuat:Autotestuat@123@192.168.10.2:3306/activity_platform?charset=utf8",#营销平台
        "BDS_DATA":"mysql+pymysql://application_aliuat:5tgb^YHN@99.48.66.40:3306/BDS_DATA?charset=utf8",  #BDS

    }
}

######### 表结构配置 ##########

table_colums = {"user_CRM.MEMBER": ("MEMBER_ID", "CREATE_TIME", "MEMBER_TYPE", "MEMBER_NAME", "MOBILE_NO"),  # 用户信息表
                "wallet_apply_info": (
                    "apply_type", "member_id", "cellphone", "identification_name", "identification_id", "apply_status",
                    "created_datetime", "apply_no", "zx_result"),  # 钱包申请表
                "wallet_money_box": ("member_id", "apply_no", "actived_datetime", "expired_date"),  # 钱柜表
                "wallet_money_box_order": (
                    "order_no", "member_id", "order_type", "status", "amount", "repayment_periods", "repayment_type",
                    "merchant_id", "store_id", "product_id", "product_name", "mobile", "allies_code",
                    "merchant_industry_type", "merchant_cl_type"),
                # 订单表
                "credit_cl_credit_limit": ("member_id", "category_id", "credit_limit", "expire_date"),  # 额度系统
                "coupon_CP_COUPON_CODE": (
                    "COUPON_ID", "COUPON_CODE", "PICK_UP_TIME", "PICK_UP_CHANNEL", "COUPON_NAME", "STATUS",
                    "MEMBER_NAME",
                    "MEMBER_PHONE", "MEMBER_ID", "COUPON_TYPE", "EFFECTIVE_TIME", "EXPIRY_TIME", "DISCOUNT", "VALUE",
                    "PERIODS", "RANGE_TYPE"),
                # 优费券表
                "user_CRM.ID_CARD": (
                    "INPUT_NAME", "INPUT_ID_NO", "MEMBER_ID", "NAME", "ID_NO", "OCR_ID_NO", "KEYIN_STATUS"),  # 身份证信息表
                "user_APPL.A_APPL": (
                    "MEMBER_ID", "APPL_AMT", "APPL_NO", "PRODUCT", "APPL_TERM", "APPL_REPAY_METHOD", "ALLIES_CODE",
                    "PROGRAM_CODE", "APPL_TIME",
                    "CLUSTER_NO", "ROLE", "EXISTING_FLAG"),
                "user_CRM.BANK_CARD": (
                    "ID", "MEMBER_ID", "CARD_NO", "NAME", "CARD_NO_SNAP", "ISSUE_BANK_NAME", "ISSUE_BANK",
                    "ISSUE_BANK_BRANCH", "CHANNEL",
                    "IS_BIND_FASTPAYMENT", "CREATE_TIME", "BANK_PHONE", "DEFAULT_USE", "CARD_TYPE", "IS_VALID",
                    "CARD_BIN",
                    "CARD_LEVEL", "ID_NO", "PURPOSE"),
                "user_FSS.ACCOUNT_CASH": ("ACCOUNT_NO", "MEMBER_ID", "MERCHANT_NO", "BALANCE"),
                "user_CRM.MEMBER_WECHAT": (
                    "MEMBER_ID", "SUBSCRIBE", "OPENID", "NICKNAME", "SEX", "LANGUAGE", "HEADIMGURL", "SUBSCRIBE_TIME",
                    "UNIONID", "FIRST_SUBSCRIBE_TIME", "LAST_UPDATE_time")
                }

######### 公关参数使用需要 ###########

phone_list = ['136', '188', '134', '135', '184', '187', '183']  # 定义号码段
card_count_sql = "select COUNT(1)  from CRM.ID_CARD where ID_NO="  # 判断id_no 是否有数据
phone_count_sql = "select COUNT(1)  from CRM.MEMBER where  MOBILE_NO="  # MOBILE_NO 是否有数据

########## 创建贷款 dubbo 配置 ############

loans_interface_name = "cn.memedai.loan.facade.business.DubboLoanCreateBusiness"
loans_method_name = "createLoan"
parameter_types = ["cn.memedai.loan.facade.request.LoanCreateForm"]
zookerpath = "zookeeper://99.48.66.13:2181"
version = '1.0.0'

categoryid = [1, 2, 3]  # 额度类别

########### 相关sql ############

merchent_sql = "select  ALLIES_NAME ,BANK_NAME ,ACCOUNT_NO,UNIONPAY_BANK_NUMBER from CRM.ALLIES where ALLIES_CODE = "

ProductInfo_sql = 'select PROGRAM_NAME,ENUM_AMT,BEGIN_AMT,END_AMT,AVAILABLE_PERIOD,AVAILABLE_REPAY_METHOD, \
                pa.APR,pf.RATE_VALUE  \
                from MKT.PROGRAM  pr  inner join CRM.ALLIES al on  pr.MERCHANT=al.ALLIES_CODE LEFT join  \
                FSS.PRICING_APR pa on pr.PROGRAM_CODE=pa.PROGRAM_CODE LEFT join  FSS.PRICING_FEE pf on pr.PROGRAM_CODE=pf.PROGRAM_CODE \
                WHERE pr.EXPIRE_TIME>GETDATE() AND pr.PROGRAM_CODE= '

REPAY_METHOD = {"554": "INSTALLMENT", "331": "AVERAGE_CAPITAL_PLUS_INTEREST"}


################# 服务器连接信息配置 ################
server_connects = {"SIT":
                       {"credit": ["99.48.66.122", 22, "mime", "mime@2016"]},
                   "ALIUAT":
                       {"credit": ["192.168.10.17", 22, "admin", "*!memeda"]}
                   }

if __name__ == '__main__':
    pass
