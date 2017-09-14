# -*- coding:utf-8 -*-
__author__ = 'Rudolf'
import COMMON
from PublicData import *

from PublicData import *
class Table_Structure ():
    def __init__(self,env='SIT'):
        self._index = -1
        self.db_name = ''
        self.OPENID = COMMON.get_OPENID()
        self.MOBILE_NO = COMMON.get_phone(env)
        self.MEMBER_ID = COMMON.get_MEMBER_ID(env)
        self.NICKNAME = COMMON.get_NickName()
        self.apply_no = COMMON.get_appl_no()

        self.create_time = COMMON.date_now()

        self.expired_date = COMMON.future_date() #将来时间


        self.loans_args = {"loanCreateCouponInfo":"","loanCreateMerchantInfo":"","loanCreateProductInfo":""}


        self.MEMBER_WECHAT_INFO = [self.MEMBER_ID, 1, self.OPENID, self.NICKNAME, '1', 'zh_CN',  \
                    'http://wx.qlogo.cn/mmopen/pUdibQO28jfy7t6dibVrbXswkwx3nMqgibwsDQ4pZ2iaQh4roCcia8tMagqZxpMl7cP8PffSOamzLBcQoqvf5nZFfuXFcTgFxdd97/0',\
                    self.create_time, self.OPENID, self.create_time, self.create_time]

        self.MEMBER_INFO = [self.MEMBER_ID, self.create_time, 1, self.NICKNAME, self.MOBILE_NO]

        self.MONEY_BOX_INFO = [self.MEMBER_ID, self.apply_no, self.create_time, self.expired_date]

    def __get_column_index(self, table_name, column):

        if table_name in table_colums.keys():
            if column in table_colums[table_name]:
                self._index = table_colums[table_name].index(column)
            elif column.lower() in table_colums[table_name]:
                self._index = table_colums[table_name].index(column.lower())


    def data_info(self, table_names, *args):
        for table_name in table_names:
            for arg in args[0]:
                self._index = -1
                self.__get_column_index(table_name, arg.split("=")[0].strip())
                if self._index != -1:
                    if '.' in table_name:
                        exec ('self.'+table_name.split('_', 1)[1].split(".", 1)[-1]+"_INFO[self._index] = str(arg.split('=')[1].strip())")
                    else:
                        exec ('self.'+table_name.split('_', 1)[1].upper()+"_INFO[self._index] = str(arg.split('=')[1].strip())")

    def loans_data(self, CouponInfo, MerchentInfo, ProductInfo):
        #用户基本信息创建：Member，id_card , 现金账户
        #创建贷款
        #放款 （各个状态）: 默认放款完成
        #构造逾期等
        loanCreateProductInfo = COMMON.get_ProductInfo(ProductInfo["PROGRAM_CODE"])

        loanCreateProductInfo["memberId"] = self.MEMBER_ID

        loanCreateProductInfo["applNo"] = self.apply_no

        loanCreateProductInfo["applDate"] = self.create_time

        loanCreateProductInfo["approvalDate"] = self.create_time

        for k, v in ProductInfo.items():
            if k == 'memberId':
                self.MEMBER_ID == v
            elif k == 'applNo':
                self.apply_no == v
            loanCreateProductInfo[k] = v

        self.loans_args["loanCreateProductInfo"] = loanCreateProductInfo

        if CouponInfo["couponIsUsed"] == "true":

            self.loans_args["loanCreateCouponInfo"] = CouponInfo

        else:
            self.loans_args["loanCreateCouponInfo"] = COMMON.get_CouponInfo()

        
        loanCreateMerchantInfo = COMMON.get_MerchantInfo(MerchentInfo["allicecode"])
        
        for k1,v1 in MerchentInfo.items():
            
            loanCreateMerchantInfo[k] = v
        
        self.loans_args["loanCreateMerchantInfo"] = loanCreateMerchantInfo
            
        
        
        #
        # try:
        #     self.__create_loans() #创建贷款
        #
        # except:
        #     print "创建贷款失败！！"
        #     sys.exit()



if __name__ == '__main__':
    t = Table_Structure('as')



