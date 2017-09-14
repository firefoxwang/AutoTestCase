# -*- coding:utf-8 -*-
from  common.basic_data import *
from  common.oprerate_db import *
from  common.Loan_Status import *
import common.config
__author__ = 'rudolf'


class Create_Loan(object):
    def __init__(self, merchent_info, loan_info, user_info=None, is_auto=True, is_account=False, is_loans=True):
        if user_info is None:
            self.member_id = gennerator_memberid()
            self.phone = generate_phone()
        else:
            self.member_id = user_info["member_id"]
            self.phone = user_info['phone']

        self.is_account = is_account

        self.openid = gennerator_openid()

        self.merchent_info = merchent_info

        self.loan_info = loan_info

        self.is_auto = is_auto

        self.nickname = gennerator_name("wixin2.0")

        self.create_time = date_now()

        self.apply_no = gennerator_applno()

        self.is_loan = is_loans

        self.loans_status = self.loan_info["loan_status"]
        self.is_overdue = self.loan_info["is_overdue"]
        self.overdue_day = self.loan_info["overdue_day"]
        self.loanCreateCouponInfo = get_CouponInfo() #优费券信息
        self.is_loans = is_loans
        self.loanCreateMerchantInfo = get_MerchantInfo(self.merchent_info["alliesCode"])

        self.loanCreateProductInfo = get_ProductInfo(self.merchent_info["PROGRAM_CODE"])
        self.member_wechat = []
        self.member_info = []
        self.source = "2"
    def __create_member_info(self):

        self.MEMBER_INFO = [self.member_id, self.create_time, 1, self.nickname, self.phone, self.source]  # 增加一个source
        self.member_info.append(dict(zip(config.table_colums["CRM.MEMBER"], self.MEMBER_INFO)))
        isnert_table("CRM.MEMBER", "user", self.member_info)

    def __create_wechart_info(self):
        self.MEMBER_WECHAT_INFO = [self.member_id, 1, self.openid, self.nickname, '1', 'zh_CN',  \
                    'http://wx.qlogo.cn/mmopen/pUdibQO28jfy7t6dibVrbXswkwx3nMqgibwsDQ4pZ2iaQh4roCcia8tMagqZxpMl7cP8PffSOamzLBcQoqvf5nZFfuXFcTgFxdd97/0',
                    self.create_time, self.openid, self.create_time, self.create_time]
        self.member_wechat.append(dict(zip(config.table_colums["CRM.MEMBER_WECHAT"], self.MEMBER_WECHAT_INFO)))
        isnert_table("CRM.MEMBER_WECHAT", "user", self.member_wechat)

    def create_loan(self):

        if self.is_auto == True and self.is_account == False:
            self.__create_member_info()
            self.__create_wechart_info()
        elif self.is_auto == False and self.is_account == True:
            self.__create_member_info()
        self.loanCreateProductInfo["memberId"] = self.member_id
        self.loanCreateProductInfo["applNo"] = self.apply_no
        self.loanCreateProductInfo["applDate"] = self.create_time
        self.loanCreateProductInfo["approvalDate"] = self.create_time
        self.loanCreateProductInfo["loanAmt"] = self.merchent_info["amount"]
        self.loans_args = {"loanCreateCouponInfo": self.loanCreateCouponInfo, "loanCreateMerchantInfo": self.loanCreateMerchantInfo, "loanCreateProductInfo": self.loanCreateProductInfo}

        create_loans(self.loans_args) #创建贷款

        if self.is_loans == True: #判断是否需要创建贷款

            loan(self.member_id, self.apply_no, self.loans_status, self.is_overdue ,self.overdue_day)
