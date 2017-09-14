# -*- coding:utf-8 -*-
__author__ = 'rudolf'

from function_library.create_loans import Create_Loan
from function_library.delete_data import *
#商户信息 必传 -- 自动化 与 功能测试
merchent_map = {"merchant_id": "100715", "store_id": "14", "product_id": "13", "amount": 2000000,
                "alliesCode": "ZKZHIXIANG", "PROGRAM_CODE": "ZKZHIXIANG_T6_CARLOAN", "repayment_type": "554",
                "repayment_periods": 6, "product_name": "宿迁中科志翔".encode('utf-8'), "PRODUCT": "CARLOAN"
            }
#账务系统构造数据 必传参数
account_merchent = {"alliesCode": "ZKZHIXIANG", "PROGRAM_CODE": "ZKZHIXIANG_T6_CARLOAN", "amount": 2000000}

#贷款信息 必传  loan_status 放款的最终状态 默认50 放款完成 ，is_overdue 是否逾期： 1 未逾期，0 逾期，overdue_day 逾期天数
loan_info = {"loan_status": 50, "is_overdue": 1, "overdue_day": 0}

# 用户信息，提供给功能测试 ,自动化测试不传
user_info = {"member_id": 1111, "phone": "13482222221"}

# is_auto=True 是否自动化 ， 默认自动化 ，功能测试传 False
# is_account 是否账务系统进行调用，默认 False  不是账务调用， True 账务调用
# is_loans=True  是否放款 ，默认放款

# 自动化测试使用方式

# cl = Create_Loan(merchent_map, loan_info)
# print cl.member_id
# cl.create_loan()
#
# Delete_Data(cl.member_id, cl.apply_no) #删除用户
#功能测试使用方式

# cl = Create_Loan(merchent_map, loan_info, user_info, is_auto=False)
#
# cl.create_loan()
# Delete_Data(cl.member_id, cl.apply_no) #删除用户
#账务构造数据 使用方式

cl = Create_Loan(account_merchent, loan_info, is_auto=False, is_account=True)
print cl.member_id
cl.create_loan()
Delete_Data(cl.member_id, cl.apply_no) #删除用户



