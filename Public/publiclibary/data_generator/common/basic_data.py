# -*- coding:utf-8 -*-
import random
from datetime import date
from datetime import timedelta
import datetime
import config
import time
from DubboLibary.DubboLib import DubboLibary
from oprerate_db import *
from dateutil.relativedelta import *
from dateutil.parser import *

'''
基础数据的生成，为后续的生成用户 与 生成流程用例 提供基础数据。
'''
__author__ = 'rudolf'

def generate_phone():
    '''
    :return: 生成全新的手机号
    '''

    prelist=["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150",
             "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    while true:
        phone = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
        phone_count = oprerate_db('user', config.sql_phone+"'"+phone+"'")
        if phone_count[0][0] > 0:
            continue
        else:
            return phone

def __getdistrictcode():
    '''
    :return: 获取区号
    '''
    with open('../file/districtcode.txt') as file:
        data = file.read()
    districtlist = data.split('\n')
    global codelist
    codelist = []
    for node in districtlist:
        #print node
        if node[10:11] != ' ':
            state = node[10:].strip()
        if node[10:11]==' 'and node[12:13]!=' ':
            city = node[12:].strip()
        if node[10:11] == ' 'and node[12:13]==' ':
            district = node[14:].strip()
            code = node[0:6]
            codelist.append({"state":state,"city":city,"district":district,"code":code})
def __gennerator():
    '''
    :return:生成ID_CARD
    '''
    __getdistrictcode()
    id = codelist[random.randint(0, len(codelist))]['code'] #地区项
    id = id + str(random.randint(1930,2013)) #年份项
    da = date.today()+timedelta(days=random.randint(1, 366)) #月份和日期项
    id = id + da.strftime('%m%d')
    id = id+ str(random.randint(100,300))#，顺序号简单处理
    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'} #校验码映射
    for i in range(0,len(id)):
        count = count + int(id[i])*weight[i]
    id = id + checkcode[str(count%11)] #算出校验码

    return id

def gennerator_card():
  '''
    :return: 返回生成新户的身份证号
  '''
  while true:
      id_card = __gennerator()
      idcard_count = oprerate_db('user', config.sql_idcard+"'"+id_card+"'")
      if idcard_count[0][0] > 0:
          continue
      else :
          return id_card

def gennerator_memberid():
    '''
    :return:生成memberid
    '''
    max_memberid = oprerate_db("user", config.sql_sequence)
    max_member_id = max_memberid[0][0]+1
    update_sequence = "update  CRM.SEQUENCE SET NEXT_VALUE="+str(max_member_id)+" where SEQ_NAME='MEMBER_ID'"
    oprerate_db("user", update_sequence)
    return max_member_id

def gennerator_applno():
    '''
    :return:生成申请编号
    '''
    appl_no = str(int(time.time()))+''+str(random.randint(1000, 9999))+str(random.randint(10, 99))
    return  appl_no

def gennerator_openid(andom_length=28):
    '''
    :return:随机生成openid
    '''
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(andom_length):
        str+=chars[random.randint(0, length)]
    return str

def gennerator_name(fist_name):
    '''
    :return:根据生成的 head_fist 姓名开头,生成姓名
    '''
    Name = str(fist_name)+str(random.randint(10, 1000))
    return Name

def date_now():
    '''
    :return:获取当前时间 时间格式: %Y-%m-%d %H:%M:%S
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def past_date(day_info):
    '''
    :param day_info:过去N天
    :return: 返回过去N天的时间 格式： %Y-%m-%d %H:%M:%S
    '''
    return time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(-int(day_info))).strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S'))

def future_date(day_info):
    '''
    :param day_info:将来的N天
    :return:返回将来N天的时间 格式： %Y-%m-%d %H:%M:%S
    '''
    return time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(int(day_info))).strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S'))

def date_new(datestr, day_info, strformat):
    strformats = ''
    times = ''
    if datestr is None or not datestr.strip():
        times = datetime.datetime.now() + datetime.timedelta(int(day_info))
    else:
        t = time.strptime(datestr, "%Y-%m-%d %H:%M:%S")
        y, m, d, h, f, s = t[0:6]
        times = datetime.datetime(y, m, d, h, f, s) + datetime.timedelta(int(day_info))
    if 1 == int(strformat):
        strformats = '%Y-%m-%d %H:%M:%S'
    elif 3 == int(strformat):
        strformats = '%Y%m%d%H%M%S'
    else:
        strformats = '%Y-%m-%d'
    return times.strftime(strformats)


def addDate_new(date_str, interval, date_format, interval_type="DAY"):
    '''
    :param date_new时间偏移datestr时间，day_info偏移天数，strformat返回日期格式
    :return:返回偏移之后的时间格式
     '''


    str_format = ''

    if date_str is None or not date_str.strip():
        times = datetime.datetime.now()
    elif isinstance(date_str, basestring):
        times = parse(date_str)
    else:
        times = date_str

    interval_type = interval_type.upper()

    if interval_type == "DAY":
        times = times + relativedelta(days=int(interval))
    elif interval_type == "MONTH":
        times = times + relativedelta(months=int(interval))
    elif interval_type == "YEAR":
        times = times + relativedelta(years=int(interval))
    else:
        times = times + relativedelta(days=int(interval))

    if 1 == int(date_format):
        str_format = '%Y-%m-%d %H:%M:%S'
    elif 3 == int(date_format):
        str_format = '%Y%m%d%H%M%S'
    elif 5 == int(date_format):
        str_format = '%Y-%m'
    else:
        str_format = '%Y%m%d'
    return times.strftime(str_format)


# 创建贷款 需要的相关信息

def get_CouponInfo(couponIsUsed = False):

    if couponIsUsed==False:

        couponInfo = {"couponIsUsed": "false"}

    else:

        couponInfo = {"couponIsUsed": "true", "couponTypeEnum": "DISCOUNT", "beforeLoanAmt": 10000, "afterLoanAmt": 9000, "merchantCompensateAmt": 800, "mimeCompensateAmt": 200}

    return couponInfo

def get_MerchantInfo(allice_code):

    merchent_info_sql = config.merchent_sql+"'"+allice_code+"'"
    merchent_infos = oprerate_db("user", merchent_info_sql)
    MerchantInfo = {"merchandiseName":'AUTO_TEST_商户',"bankAccountName":"AUTO_TEST_银行","bankAccountNo":merchent_infos[0][2],"creditLimitCategoryId":'1',"merchantName":"TEST","storeName":"12","subItemId":"12","subItemName":"TEST","bankName":"招商银行","bankBranchName":"招商银行","bankCity":"上海","alliesCode":"ZKZHIXIANG"}
    # 暂时修改一下 加一个 "alliesCode":"ZKZHIXIANG"  alliescode字段不能为空
    return MerchantInfo


def get_ProductInfo(PROGRAM_CODE):
    Product_Info_sql = config.ProductInfo_sql +"'"+PROGRAM_CODE+"'"
    print Product_Info_sql
    Product_Info = oprerate_db("user", Product_Info_sql)
    REPAY_METHOD_ = config.REPAY_METHOD[Product_Info[0][5].replace('[','').replace(']','')]
    print Product_Info[0][6]
    if Product_Info[0][6] == None:
        apr = 0.000001
    else:
        apr = float(str(Product_Info[0][6]))

    if Product_Info[0][7] == None:
        loanFeeApr = 0.0
    else:
        loanFeeApr = float(str(Product_Info[0][7]))
    print apr, loanFeeApr
    ProductInfo ={"memberId": "", "applNo": "",
                  "applDate": "", "approvalDate": "",
                  "rating": "A", "productName": '', "productId": "", "loanAmt": int(Product_Info[0][3]),
                  "repayMethodEnum": REPAY_METHOD_, "apr": apr,
                  "loanPeriod": Product_Info[0][4].replace('[', '').replace(']', ''), "loanFeeApr": loanFeeApr, "capitalNo": "001"}
    return ProductInfo


def create_loans(loans_args):
    DL = DubboLibary()
    DL.connect_to_dubbo_register(config.zookerpath)
    duresult = DL.call_dubbo_interface_method(config.loans_interface_name, config.loans_method_name, config.parameter_types, config.version, str(loans_args))



