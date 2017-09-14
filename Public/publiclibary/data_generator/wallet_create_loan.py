# -*- coding:utf-8 -*-
from function_library.create_loans import Create_Loan
from function_library.delete_data import *
import sys
__author__ = 'rudolf'

def wallet_create_loan(merchent_infos,loan_infos,user_infos):
    '''
    :param merchent_info: 输入参数格式 与内容 ： {"merchant_id": "100715", "store_id": "14", "product_id": "13", "amount": 2000000,
                "alliesCode": "ZKZHIXIANG", "PROGRAM_CODE": "ZKZHIXIANG_T6_CARLOAN", "repayment_type": "554",
                "repayment_periods": 6, "product_name": "宿迁中科志翔".encode('utf-8'), "PRODUCT": "CARLOAN"
            }
    :param loan_info: 输入参数的格式与内容：{"loan_status": 50, "is_overdue": 1, "overdue_day": 0}
                    贷款信息 必传  loan_status 放款的最终状态 默认50 放款完成 ，is_overdue 是否逾期： 1 未逾期，0 逾期，overdue_day 逾期天数
    :return: 返回 是创建贷款的对象 ，可以通过 对象+属性获取值例如 对象为cl 则获取值member_id 与apply_no 的方法  ：cl.member_id, cl.apply_no
    '''

    if isinstance(merchent_infos, dict):
        merchent_map = merchent_infos
    elif isinstance(merchent_infos, (unicode, str)):
        if "{" in merchent_infos and  "}" in merchent_infos:
            merchent_map = eval(merchent_infos)
        else:
            print "参数格式错误！！参数 ： {a:b,a:b}"
            sys.out()
    else:
        print "参数格式错误！！参数 ： {a:b,a:b}"
        sys.out()

    if isinstance(loan_infos, dict):
        loan_map = loan_infos

    elif isinstance(loan_infos, (unicode, str)):
        if "{" in loan_infos and "}" in loan_infos:
            loan_map = eval(loan_infos)
        else:
            print "参数格式错误！！参数 ： {a:b,a:b}"
            sys.out()
    else:
        print "参数格式错误！！参数 ： {a:b,a:b}"
        sys.out()

    if isinstance(user_infos, dict):
        user_= user_infos

    elif isinstance(user_infos, (unicode, str)):
        if "{" in user_infos and "}" in user_infos:
            user_ = eval(user_infos)
        else:
            print "参数格式错误！！参数 ： {a:b,a:b}"
            sys.out()
    else:
        print "参数格式错误！！参数 ： {a:b,a:b}"
        sys.out()
    cl = Create_Loan(merchent_info=merchent_map,loan_info=loan_map,user_info=user_,is_auto=False)
    cl.create_loan()
    return cl

