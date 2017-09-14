# -*- coding:utf-8 -*-
from function_library.create_loans import Create_Loan
from function_library.delete_data import *
import sys
__author__ = 'rudolf'

def auto_create_loan(merchent_info, loan_info):
    '''
    :param merchent_info: 输入参数格式 与内容 ： {"merchant_id": "100715", "store_id": "14", "product_id": "13", "amount": 2000000,
                "alliesCode": "ZKZHIXIANG", "PROGRAM_CODE": "ZKZHIXIANG_T6_CARLOAN", "repayment_type": "554",
                "repayment_periods": 6, "product_name": "宿迁中科志翔".encode('utf-8'), "PRODUCT": "CARLOAN"
            }
    :param loan_info: 输入参数的格式与内容：{"loan_status": 50, "is_overdue": 1, "overdue_day": 0}
                    贷款信息 必传  loan_status 放款的最终状态 默认50 放款完成 ，is_overdue 是否逾期： 1 未逾期，0 逾期，overdue_day 逾期天数
    :return: 返回 是创建贷款的对象 ，可以通过 对象+属性获取值例如 对象为cl 则获取值member_id 与apply_no 的方法  ：cl.member_id, cl.apply_no
    '''

    if isinstance(merchent_info, dict):
        merchent_map = merchent_info
    elif isinstance(merchent_info, (unicode, str)):
        if "{" in merchent_info and  "}" in merchent_info:
            merchent_map = eval(merchent_info)
        else:
            print "参数格式错误！！参数 ： {a:b,a:b}"
            sys.out()
    else:
        print "参数格式错误！！参数 ： {a:b,a:b}"
        sys.out()

    if isinstance(loan_info, dict):
        loan_map = loan_info

    elif isinstance(loan_info, (unicode, str)):
        if "{" in loan_info and "}" in loan_info:
            loan_map = eval(loan_info)
        else:
            print "参数格式错误！！参数 ： {a:b,a:b}"
            sys.out()
    else:
        print "参数格式错误！！参数 ： {a:b,a:b}"
        sys.out()


    cl = Create_Loan(merchent_map, loan_map, is_auto=True)
    cl.create_loan()
    return cl

