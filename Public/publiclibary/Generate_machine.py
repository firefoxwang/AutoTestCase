# -*- coding:utf-8 -*-
import random
import time
from sqlalchemy import *
from PublicData import *
import logging

"""
此文件用来随机生成米么的各种随机数据
"""


def __oprerate_db(db_type, sql, env='SIT'):
    engine = create_engine(db_connects[env.upper()][db_type], echo=False)

    return_info = None

    # todo 临时规避首次连接数据丢失连问题
    flag=1
    while (flag<2):
        try:
            engine.connect()
            break
        except:
            flag=flag+1

    try:
        if 'mysql' in db_connects[env.upper()][db_type]:
            # '若有主外键约束，先取消设置，然后设置'
            engine.execute("SET FOREIGN_KEY_CHECKS=0 ")
            if 'select' in sql.lower():
                return_info = engine.execute(sql).fetchall()
            else:
                engine.execute(sql)
            engine.execute("SET FOREIGN_KEY_CHECKS=1 ")
        else:
            if 'select' in sql.lower():
                return_info = engine.execute(sql).fetchall()
            else:
                engine.execute(sql)
    except Exception, e:
        logging.exception('caught an error')
        print "Exception:", e
    finally:
        engine.connect().close()
        return return_info


def get_name():
    name = u'自动化测试'+str(random.randint(10,1000))
    return name

def __generate_idcard():
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

    u''' 随机生成新的18为身份证号码 '''
    t = time.localtime()[0]

    x = '%02d%02d%02d%04d%02d%02d%03d' % (random.randint(10, 99),
                                          random.randint(01, 99),
                                          random.randint(01, 99),
                                          random.randint(t - 50, t - 18),
                                          random.randint(1, 12),
                                          random.randint(1, 28),
                                          random.randint(1, 999))

    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]

    id_card = '%s%s' % (x, LAST[y % 11])

    return id_card


def __generate_phone():
    phone = random.choice(phone_list) + "".join(random.choice("0123456789") for i in range(8))

    return phone


def get_MEMBER_ID(env='SIT'):
    # max_member_id=80001
    """

    :param env:  SIT或者ALIUAT  可以不填
    :return: 返回会员ID
    """
    max_memberid = __oprerate_db("user", "select NEXT_VALUE  from  CRM.SEQUENCE  where SEQ_NAME='MEMBER_ID' ", env)
    max_member_id = max_memberid[0][0] + 1
    update_sequence = "update  CRM.SEQUENCE SET NEXT_VALUE=" + str(max_member_id) + " where SEQ_NAME='MEMBER_ID'"
    __oprerate_db("user", update_sequence, env)
    return max_member_id


def get_idcard(env='SIT'):
    var = 1
    while var == 1:
        id_card = __generate_idcard()
        card_count = __oprerate_db("user", "select COUNT(1)  from CRM.ID_CARD where ID_NO=" + "'" + id_card + "'", env)
        if int(card_count[0][0]) == 0:
            id_card_ = id_card
            break
    return id_card


def get_appl_no():
    appl_no = str(int(time.time())) + '' + str(random.randint(1000, 9999)) + str(random.randint(10, 99))

    return appl_no


def get_OPENID(random_length=28):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def get_phone(env='SIT'):
    var = 1
    while var == 1:
        phone = __generate_phone()
        phone_count = __oprerate_db("user", "select COUNT(1)  from CRM.MEMBER where  MOBILE_NO=" + "'" + phone + "'",
                                    env)
        if int(phone_count[0][0]) == 0:
            phone_ = phone
            break
    return phone_


def auto_machine(env='SIT'):
    """

    :return: member_id,phone,id_card,appl_no,oder_no_merchandise（商城的主订单），orderNo
    调用方式： 赋值后直接从里面拿对应的key  ${a} auto_machine  ${member_id}=get from dictionary ${a}
    """
    member_id = get_MEMBER_ID(env)
    phone = get_phone(env)
    id_card = get_idcard(env)
    appl_no = get_appl_no()
    oder_no_merchandise = '110' + str(appl_no)
    orderNo = get_appl_no()
    name = get_name()
    mime_dict = {"member_id": member_id, "phone": phone, "id_card": id_card, "appl_no": appl_no,
                 "oder_no_merchandise": oder_no_merchandise, "orderNo": orderNo, "name": name}
    return mime_dict


def inster_user_image(name, memberid, idcard, env='SIT'):
    """

    :param name:
    :param memberid:
    :param idcard:
    :param env: 默认sit
    """
    sql_idcard = "INSERT INTO crm.ID_CARD([MEMBER_ID], [OCR_NAME], [OCR_SEX], [OCR_NATIONALITY], [OCR_BIRTHDAY], [OCR_ADDRESS], [OCR_ID_NO], [OCR_ISSUER], [OCR_VALID_FROM], [OCR_VALID_THRU], [IMAGE_FRONT], [IMAGE_BACK], [NAME], [SEX], [NATIONALITY], [BIRTHDAY], [ADDRESS], [ID_NO], [ISSUER], [VALID_FROM], [VALID_THRU], [ID_PROVINCE], [ID_CITY], [ID_AREA], [ADDRESS_PROVINCE], [ADDRESS_CITY], [CREATE_TIME], [IS_VERIFIED], [VERIFIED_TIME], [OPERATOR], [KEYINER], [KEYIN_TIME], [KEYIN_STATUS], [INPUT_NAME], [INPUT_ID_NO], [UPLOAD_STATUS], [IS_VALID], [PHOTO_QUALITY], [OSS_FILE_FRONT], [OSS_FILE_BACK], [SAVE_TYPE], [FRONT_UPLOAD_STATUS], [BACK_UPLOAD_STATUS], [ID_VALID_STATUS]) VALUES ('{1}', '{0}', '1', '汉', '1987-09-29 00:00:00', '南京市鼓楼区狗耳巷42号丐01室', '{2}', '南京市公安局鼓楼分局', '2011-02-10', '2021-02-10', NULL, NULL, '{0}', '1', '汉', '1987-09-29 00:00:00', '南京市鼓楼区狗耳巷42号丐01室', '{2}', '南京市公安局鼓楼分局', '2011-02-10', '2021-02-10', '江苏', '南京', '江苏省南京市鼓楼区', NULL, NULL, GETDATE(), NULL, NULL, NULL, 'C41001', '2017-04-28 13:38:01.800', '1', '{0}', '{2}', '0', '0', NULL, '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '2100_NW5HD4O-KGEKZB0RRVLPD1FBO9Q83-LB84G12J-0.jpg', '1', '1', '1', '1');".format(
        name, memberid, idcard)
    sql_image_log_1001 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE]) VALUES ( '{0}', '1001', '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1002 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE]) VALUES ( '{0}', '1002', '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1005 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE]) VALUES ( '{0}', '1005', '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1004 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE]) VALUES ( '{0}', '1004', '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1010 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE]) VALUES ( '{0}', '1010', '2100_NW5HD4O-KGEK0VGXPPJXRLIBDV7T1-S3Z3G12J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_1001 = "INSERT INTO CRM.MEMBER_IMAGE ([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE]) VALUES ('{0}', '1001', '1', '2000_R9866S71-ACEK2E4HU5Y24CSM2VBP1-UNA4A12J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', GETDATE(), '1');".format(
        memberid)
    sql_image_1002 = "INSERT INTO CRM.MEMBER_IMAGE ([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE]) VALUES ('{0}', '1002', '1', '2000_R9866S71-ACEK2E4HU5Y24CSM2VBP1-UNA4A12J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', GETDATE(), '1');".format(
        memberid)
    sql_image_1004 = "INSERT INTO CRM.MEMBER_IMAGE ([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE]) VALUES ('{0}', '1005', '1', '2000_R9866S71-ACEK2E4HU5Y24CSM2VBP1-UNA4A12J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', GETDATE(), '1');".format(
        memberid)
    sql_image_1005 = "INSERT INTO CRM.MEMBER_IMAGE ([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE]) VALUES ('{0}', '1004', '1', '2000_R9866S71-ACEK2E4HU5Y24CSM2VBP1-UNA4A12J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', GETDATE(), '1');".format(
        memberid)
    sql_image_1010 = "INSERT INTO CRM.MEMBER_IMAGE ([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE]) VALUES ('{0}', '1010', '1', '2000_R9866S71-ACEK2E4HU5Y24CSM2VBP1-UNA4A12J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', GETDATE(), '1');".format(
        memberid)
    sql_image_log_1021 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE])  VALUES ( '{0}', '1021', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1022 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE])  VALUES ( '{0}', '1022', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1023 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE])  VALUES ( '{0}', '1023', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_log_1024 = "INSERT INTO crm.MEMBER_IMAGE_log ( [MEMBER_ID], [IMAGE_TYPE], [IMAGE_FILENAME], [SAVE_TYPE], [MEDIA_ID], [WECHAT], [UPLOAD_TIME], [UPLOAD_IP], [TEMP_FILE])  VALUES ( '{0}', '1024', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', '1', NULL, NULL, GETDATE(), NULL, NULL);".format(
        memberid)
    sql_image_1021 = "INSERT INTO CRM.MEMBER_IMAGE([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE])  VALUES ('{0}', '1021', '1', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', NULL, '1');".format(
        memberid)
    sql_image_1022 = "INSERT INTO CRM.MEMBER_IMAGE([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE])  VALUES ('{0}', '1022', '1', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', NULL, '1');".format(
        memberid)
    sql_image_1023 = "INSERT INTO CRM.MEMBER_IMAGE([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE])  VALUES ('{0}', '1023', '1', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', NULL, '1');".format(
        memberid)
    sql_image_1024 = "INSERT INTO CRM.MEMBER_IMAGE([MEMBER_ID], [IMAGE_TYPE], [IMAGE_NO], [IMAGE_FILENAME], [UPLOAD_TIME], [UPLOAD_IP], [MEDIA_ID], [WECHAT], [REDOWNLOAD], [UPDATE_TIME], [SAVE_TYPE])  VALUES ('{0}', '1024', '1', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', GETDATE(), NULL, NULL, NULL, '0', NULL, '1');".format(
        memberid)
    sql_face = "INSERT INTO CRM.FACE_VALIDATE_LOG ( [MEMBER_ID], [SOURCE], [CREATE_TIME], [CREDIT_RESULT], [IMG_0], [IMG_1], [IMG_2], [IMG_3], [IP], [IP_CITY], [IP2], [IP2_CITY], [IP_NET], [IMSI], [IMEI], [MAC], [IDFA], [UUID], [DEVICE_ID], [LATITUDE], [LONGITUDE], [PROVINCE], [CITY], [COUNTY], [ADDRESS], [ACTIVITY_NO], [ID_NO], [NAME], [PRODUCT], [CLIENT_CHANNEL])  VALUES ( '{0}','1', GETDATE(), '0', '2000_TLFK8Z-1RHJCCE7RMJE92YYYKS93-VN13IR0J-0.jpg', '2000_TLFK8Z-9J4JRQXSQEVCK3XSHYGB2-7MWRX80J-0.jpg', '2000_TLFK8Z-FO4JMPG7PNCOF31XF1EH3-Y5Y0590J-0.jpg', '2000_TLFK8Z-OOKIUZ14U2JLK3RAX44M2-X3E12HZI-0.jpg', '117.136.45.139', '南京市', NULL, NULL, '', NULL, '865479023217680', NULL, NULL, NULL, '865479023217680', NULL, NULL, NULL, NULL, NULL, NULL, '149326366000499545927', '{1}', '{2}', 'cashloan', '10');".format(
        memberid, idcard, name)
    sql_image_ = [sql_idcard, sql_image_log_1001, sql_image_log_1002, sql_image_log_1004, sql_image_log_1005,
                  sql_image_log_1010, sql_image_1001, sql_image_1002, sql_image_1004, sql_image_1005, sql_image_1010,
                  sql_image_log_1021, sql_image_log_1022, sql_image_log_1023, sql_image_log_1024, sql_image_1021,
                  sql_image_1022, sql_image_1023, sql_image_1024, sql_face]
    for i in sql_image_:
        print(u"插入的sql语句为  ", i)
        __oprerate_db("user", i, env)


def insert_user(memberid, phone, name, env='SIT'):
    """
    插入会员相关数据，包括联系人跟jxl,member表
    :param memberid:
    :param phone:
    :param name:
    :param env: 默认sit
    """
    sql_member = "INSERT INTO [memedaidb].[CRM].[MEMBER] ([MEMBER_ID], [CREATE_TIME], [MEMBER_TYPE], [MEMBER_NAME], [SEX], [MOBILE_NO], [MARITAL_STATUS], [EDUCATION], [INDUSTRY], [EMAIL], [EMAIL_VERIFIED], [SCHOOL_ID], [GRADE], [PRE_CRL], [PRE_SCORE], [PRE_RATING], [PRE_SCORE_TIME], [INCOME], [HOME_TELE_NO], [CONTACTS_NAME1], [CONTACTS_PHONE1], [CONTACTS_NAME2], [CONTACTS_PHONE2], [SALES], [PROMOTE], [PROMOTE_GROUP], [PROMOTE_MEMO], [SCORE], [LAST_SCORE_VER], [RATING], [CREDIT_LINE], [LAST_SCORE_TIME], [LAST_CREDIT_TIME], [EXISTING_FLAG], [MEMBER_ROLE_FLAG], [BLOCK_CODE], [BLOCK_TIME], [STATUS], [LAST_UPDATE], [OPERATOR], [QQ], [CITY], [COMPANY], [FAX], [WEBSITE], [POSITION], [CC], [OC], [UNIV_PROVINCE], [UNIV_CITY], [UNIV], [DEGREE], [DEPARTMENT], [MAJOR], [CLASS], [LENGTH_SCHOOL], [ENROLLMENT_TIME], [GRADUATION_TIME], [STUDENT_ID], [HOME_ADDRESS], [ROOM_ADDRESS], [LAST_REJECTED_TIME], [LABEL], [DELQ24], [LAST_LOAN_DATE], [MEMBER_WC_NO], [FROM_CHANNEL], [DUTY], [MERCHANT_CONFIRM], [HEADIMGURL], [NICKNAME], [SOURCE], [RESIDENTIALPROVINCE], [RESIDENTIALCITY], [RESIDENTIALDISTRICT], [RESIDENTIALADDRESS], [CONTACTS_RELATION1], [CONTACTS_RELATION2], [IS_STUDENT], [HOME_PROVINCE], [HOME_CITY], [HOME_COUNTY], [REGISTER_CLIENT], [REGISTER_STORE], [LAST_UPDATE_TIME]) VALUES ('{0}', GETDATE(), '1', '{2}', '1', '{1}', NULL, '4', '41', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '0', NULL, '青霞', '18351905242', '', '', NULL, 'mmd_11_8229', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', '0', '', NULL, '0', GETDATE(), NULL, NULL, NULL, '米么金服', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', NULL, NULL, '2', NULL, NULL, NULL, NULL, NULL, NULL, '0', NULL, NULL, NULL, '11', '8229', GETDATE());".format(
        memberid, phone, name)
    sql_contant = "INSERT INTO crm.CONTACT_VALIDATE_LOG ( [MEMBER_ID], [SOURCE], [PRODUCT], [CREATE_TIME], [RESULT], [REMARK], [ACTIVITY_NO]) VALUES ('{0}', NULL, NULL, GETDATE(), '0', NULL, '149327606655599545924');".format(
        memberid)
    sql_jxl = "INSERT INTO crm.JXL_VALIDATE_LOG( [MEMBER_ID], [SOURCE], [PRODUCT], [CREATE_TIME], [CREDIT_RESULT], [PASSWORD], [ACCOUNT], [JXL_TYPE], [TOKEN], [SERIAL_NO], [REMARK], [ACTIVITY_NO]) VALUES ('{0}', '1', 'cashloan', GETDATE(), '0', '236444667E547C3A79E7C6ACD8190606', '18351905245', '3', '21e4a1d238af4cbd9eda1a308a116fd2', '149328625812099545927', NULL, NULL);".format(
        memberid)
    sql_user = [sql_member, sql_contant, sql_jxl]
    for i in sql_user:
        print(u"插入的sql语句为  ", i)
        __oprerate_db("user", i, env)


def get_merchandiseinfo(allies_code, periods, env='SIT'):
    """

    :param allies_code: 1234_3455
    :param periods: 期数 3 6 9 12 24
     :param env: 默认sit
    :return: 返回商户相关的字典
    """
    if isinstance(allies_code, (str, unicode)) and allies_code.find('_') and isinstance(periods, (int, str, unicode)):
        merchantid = allies_code[:allies_code.find('_')]
        shopid = allies_code[(allies_code.find('_')+1):]
        sql_merchant_industry_type = "SELECT id FROM  ma_merchant_template WHERE first_type=(SELECT sec_template_type FROM ma_merchant_baseinfo WHERE merchantid  = '{0}')".format(
            merchantid)
        merchant_industry_type = (__oprerate_db("merchant", sql_merchant_industry_type, env))[0][0]
        sql_merchandise = "SELECT `merchandiseid` FROM `ma_merchandise_baseinfo` WHERE  merchantid  = '{0}'".format(
            merchantid)
        merchandise_result = (__oprerate_db("merchant", sql_merchandise, env))
        merchandiseid = merchandise_result[0][0]
        sql_apr_result = "SELECT total_fee_rate,pre_fee_rate FROM ma_merchandise_subitem WHERE period_num = '{1}' AND merchandiseid = (SELECT `merchandiseid` FROM `ma_merchandise_baseinfo` WHERE  merchantid  = '{0}')".format(
            merchantid, periods)
        apr_result = (__oprerate_db("merchant", sql_apr_result, env))
        apr = apr_result[0][0]
        p_loan_fee_apr = apr_result[0][1]
        merchandiseinfo_dict = {"merchantid": int(merchantid), "merchant_industry_type": int(merchant_industry_type), "apr": float(apr),
                                "p_loan_fee_apr": float(p_loan_fee_apr), "shopid": shopid, "merchandiseid": int(merchandiseid)}
        return merchandiseinfo_dict
    else:
        print(u"传入allies_code或periods格式错误")
        return None


def insert_order(allies_code, order_no, base_order_no, member_id, amount, mobile, periods,
                 env="SIT", ):
    """

    :param allies_code:
    :param order_no:
    :param base_order_no:
    :param member_id:
    :param amount:
    :param periods:
    :param mobile:
    :param periods:
    :param env:  默认值
    :return:
    """
    merchandiseinfo_dict = get_merchandiseinfo(allies_code, periods, env)
    merchant_id = merchandiseinfo_dict["merchantid"]
    store_id = merchandiseinfo_dict["shopid"]
    merchant_industry_type = merchandiseinfo_dict["merchant_industry_type"]
    product_id = merchandiseinfo_dict["merchandiseid"]
    p_loan_fee_apr = merchandiseinfo_dict["p_loan_fee_apr"]
    apr = merchandiseinfo_dict["apr"]
    sql = """INSERT INTO `money_box_order` ( `order_no`, `base_order_no`, `member_id`, `order_type`, `merchant_order_id`, `status`, `amount`, `confirm_amount`, `audit_amount`, `pay_expire_datatime`, `repayment_periods`, `repayment_type`, `capital_no`, `merchant_id`, `store_id`, `product_id`, `store_lat`, `store_lon`, `member_lat`, `member_lon`, `ip`, `imei`, `created_datetime`, `modified_datetime`, `product_name`, `mobile`, `channel`, `merchant_order_createdtime`, `discount_amount`, `pay_amount`, `merchant_industry_type`, `merchant_cl_type`, `allies_code`, `merchant_head_url`, `merchant_name`, `cz_patch_mq`, `cz_result_mq`, `store_name`, `p_apr`, `p_loan_fee_apr`, `c_approved_date_time`, `channel_type`, `source`, `version`, `seller_no`, `open_id`, `td_id`, `p_apr_amt`, `p_loan_fee_apr_amt`, `expired_date`, `start_rent_date`, `receipt_addr`, `receipt_name`, `receipt_phone`, `audited_datetime`, `merchant_full_name`, `apr`, `product_info`, `ship_info`, `project_type`, `product_type`, `apply_source`, `activity_no`) VALUES ( '{0}', '{1}', '{2}', '0', NULL, '1051', '{3}', '{3}', NULL, NOW(), '{4}', '554', '023', '{5}', '{6}', '{7}', NULL, NULL, NULL, NULL, NULL, NULL,NOW(), NOW(), 'O2O商户5', '{8}', '{{channel:11, merchantId:{5}, storeId:{6}, sellerNo:"null", appId:"null"}}', NULL, '0', '{3}', '{9}', '1', '{10}', 'https://aliuat.memedai.cn/merchant_nj/img/ab/5a/d00b15fdfc7d424f821d62a70def.png', '公司地址默认值测试分', '{{"patchMemo":"","memberId":{2},"orderId":{0},"patchList":[{{"content":"","fileType":"1","name":"合同","code":"BP001"}}]}}', '{{"decision":"3","desc":"","orderId":"{1}","patches":[{{"code":"BP001","url":["2000_R9866S71-OQDMZ6NQNVN5X0YZ37B03-JQIMKT4J-0.jpg"]}}]}}', '米么测试门店(医美消费)', '0.000000', '{11}', NOW(), '0', '11', '2.0', NULL, NULL, NULL, '1000.00', '1100.00', '2097-07-14', NULL, NULL, NULL, NULL, '2017-07-07 15:59:03', 'O2O商户5', '{12}', "{{\'merchandiseInfo\':[{{\'merchandiseLogo\':\'https://aliuat.memedai.cn/merchant_nj/img/ab/5a/d00b15fdfc7d424f821d62a70def.png\',\'merchandiseName\':\'O2O商户5\',\'merchandiseId\':'{7}',\'merchandiseCount\':1,\'merchandisetAmount\':'{3}'}}],\'merchantType\':0,\'freight\':0}}", NULL, '皮肤|除皱/纹', NULL, NULL, NULL);""".format(
        order_no, base_order_no, member_id, amount, periods, merchant_id, store_id, product_id, mobile,
        merchant_industry_type, allies_code, p_loan_fee_apr, apr
    )
    print sql
    __oprerate_db("wallet", sql, env)



if __name__ == '__main__':
    auto_machine('sit')