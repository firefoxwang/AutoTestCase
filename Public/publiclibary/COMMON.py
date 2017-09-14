# -*- coding:utf-8 -*-

'''
此文件 相关数据 的自动生成
'''
import random
import time
from PublicData import *
import datetime
from sqlalchemy import *



def __oprerate_db (db_type, sql, env='SIT'):

    '''
    Delinfo_By_Sql 通过sql 语句删除 数据  \n
        参数 db_type :数据库链接 （user） --如需新增 请在 ReferenceData 文件下按照格式新增  \n
    sql 执行的 sql 语句 \
        使用方法 : Delinfo By Sql | user | delete from xxx where xxxx | \n
    '''

    engine = create_engine(db_connects[env][db_type], echo=False)

    return_info = None

    # 临时规避首次连接数据丢失连问题
    flag=1
    while (flag<2):
        try:
            engine.connect()
            break
        except:
            flag=flag+1

    try:
        if 'mysql' in db_connects[env][db_type]:
            #'若有主外键约束，先取消设置，然后设置'
            engine.execute("SET FOREIGN_KEY_CHECKS=0 ")
            if 'select' in sql:
                return_info = engine.execute(sql).fetchall()
            else:
                engine.execute(sql)
            engine.execute("SET FOREIGN_KEY_CHECKS=1 ")
        else:
            if 'select' in sql:
                return_info = engine.execute(sql).fetchall()
            else:
                engine.execute(sql)
    except Exception, e:

        print "Exception:", e

    return return_info


def __generate_phone():

    phone = random.choice(phone_list)+"".join(random.choice("0123456789") for i in range(8))

    return phone

def __generate_idcard():

    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

    u''' 随机生成新的18为身份证号码 '''
    t = time.localtime()[0]

    x = '%02d%02d%02d%04d%02d%02d%03d' %(random.randint(10,99),
                                        random.randint(01,99),
                                        random.randint(01,99),
                                        random.randint(t - 50, t - 18),
                                        random.randint(1,12),
                                        random.randint(1,28),
                                        random.randint(1,999))

    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]

    id_card='%s%s' %(x, LAST[y % 11])

    return id_card

def get_appl_no():

    appl_no = str(int(time.time()))+''+str(random.randint(1000, 9999))+str(random.randint(10, 99))

    return appl_no

def get_cashappl_no():

    appl_no = str('05')+str(int(time.time()))+''+str(random.randint(1000, 9999))

    return appl_no

def get_OPENID(random_length=28):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(random_length):
        str+=chars[random.randint(0, length)]
    return str

def get_phone(env='SIT'):
    var = 1
    while var == 1:
        phone = __generate_phone()
        phone_count=__oprerate_db("user",phone_count_sql+"'"+phone+"'",env)
        if int(phone_count[0][0]) == 0:
            phone_ = phone
            break
    return phone_

def get_MEMBER_ID(env='SIT'):

    #max_member_id=80001
    max_memberid = __oprerate_db("user","select NEXT_VALUE  from  CRM.SEQUENCE  where SEQ_NAME='MEMBER_ID' ",env)
    max_member_id=max_memberid[0][0]+1
    update_sequence="update  CRM.SEQUENCE SET NEXT_VALUE="+str(max_member_id)+" where SEQ_NAME='MEMBER_ID'"
    __oprerate_db("user",update_sequence,env)
    return max_member_id

def get_NickName():
    NickName = 'wechat2.0_0'+str(random.randint(10,1000))
    return NickName

def get_idcard(env='SIT'):
    var = 1
    while var == 1:
        id_card = __generate_idcard()
        card_count=__oprerate_db("user",card_count_sql+"'"+id_card+"'",env)
        if int(card_count[0][0])==0:
            id_card_ = id_card
            break
    return id_card

# 创建贷款 需要的相关信息

def get_CouponInfo(couponIsUsed = False):

    if couponIsUsed==False:

        couponInfo = {"couponIsUsed":"false"}

    else:

        couponInfo = {"couponIsUsed":"true","couponTypeEnum":"DISCOUNT","beforeLoanAmt":10000,"afterLoanAmt":9000,"merchantCompensateAmt":800,"mimeCompensateAmt":200}

    return couponInfo

def get_MerchantInfo(allice_code):

    merchent_info_sql = merchent_sql+"'"+allice_code+"'"
    merchent_infos = __oprerate_db("user", merchent_info_sql)
    MerchantInfo = {"merchandiseName":'AUTO_TEST_商户',"bankAccountName":"AUTO_TEST_银行","bankAccountNo":merchent_infos[0][2],"creditLimitCategoryId":'1',"merchantName":"TEST","storeName":"12","subItemId":"12","subItemName":"TEST","bankName":"招商银行","bankBranchName":"招商银行","bankCity":"上海","alliesCode":"ZKZHIXIANG"}
    #  暂时修改一下，加个"alliesCode":"ZKZHIXIANG"

    return MerchantInfo


def get_ProductInfo(PROGRAM_CODE):
    Product_Info_sql=ProductInfo_sql +"'"+PROGRAM_CODE+"'"
    Product_Info = __oprerate_db("user", Product_Info_sql)
    REPAY_METHOD_ = REPAY_METHOD[Product_Info[0][5].replace('[','').replace(']','')]
    print Product_Info
    if str(Product_Info[0][6]) == None:
        apr =0.000001
    else:
        apr=float(str(Product_Info[0][6]))

    if str(Product_Info[0][7]) == None:
        loanFeeApr=0.0
    else:
        loanFeeApr=float(str(Product_Info[0][7]))
    print apr , loanFeeApr
    ProductInfo ={"memberId":"","applNo":"",
                  "applDate":"","approvalDate":"",
                  "rating":"A","productName":'',"productId":"","loanAmt":int(Product_Info[0][3]),
                  "repayMethodEnum":REPAY_METHOD_,"apr":apr,
                  "loanPeriod":Product_Info[0][4].replace('[','').replace(']',''),"loanFeeApr":loanFeeApr,"capitalNo":"001"}
    return ProductInfo

def date_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def past_date():
    '格式为 %Y-%m-%d %H:%M:%S'
    return time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(-7)).strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S'))
def future_date():
    '格式为 %Y-%m-%d %H:%M:%S'
    return time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(7)).strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S'))
def past_date_1():
    '格式为 %Y-%m-%d '
    return (datetime.datetime.now()+datetime.timedelta(-7)).strftime("%Y-%m-%d")

def future_date_1():
    return (datetime.datetime.now()+datetime.timedelta(7)).strftime("%Y-%m-%d")

def pay_date():
    return time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(30)).strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S'))

