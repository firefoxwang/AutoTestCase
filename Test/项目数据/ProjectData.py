# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import RF_ENV

'''
Created on 2016-11-20

@author: wanglingbo



'''

# 接口相关配置

api_host = "https://aliuat.memedai.cn"

heard_info_app = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                  'mmDeviceId': '28461FB5-1916-4704-B199-4E5ECE463339', 'mmAppId': '8bd5b7be4dd308ecd3be7e1cefd5246b',
                  'mmChannel': 'mmdApp_ios', 'Content-Type': 'application/json; charset=UTF-8', 'appCode': 'cvdc06mB8g5OqQBctSt_ogb4ixGAAB','thdUserId':'F3F70CFA4AF610F19FD06E0EEB920B74E7A45CF66EB1F72E1E94B78676F7DCD8'}  #'appcode'是sdk字头的商户 htdUserld是手机号的加密

api_url = {"getPublicKey": "/user/common/getPublicKey",  # 公钥获取
           "user_login": "/user/login/phoneLogin",  # 动码登录
           "user_app_login": "/user/login/v3/in",  # user 密码登录
           "user_publickey": "/user/v2/common/getPublicKey",  # key
           "user_loginByPhone": "/user/login/phoneLogin",  # 动码登录
           "sendPhoneVerifyCode": "/walletApp/common/sendPhoneVerifyCode",  # 钱包获取登录验证码
           "phoneLogin": "/user/login/v3/phoneLogin",  # 动码登录
           "getApplicationInfo": "/sdk-web/v1/common/getApplicationInfo",  # 获取App信息
           "getMobileNo": "/sdk-web/v1/login/getMobileNo",  # 获取手机号
           "authorise": "/sdk-web/v1/common/authorise",  # 静默授权
           "submitMerchantOrder": "/sdk-web/v1/order/submitMerchantOrder",  # 创建钱包订单
           "submitApplyInfo": "/sdk-gateway/v1/order/submitApplyInfo",  # 预申请
           "submitMemberInfo": "/sdk-web/v1/apply/submitMemberInfo",  # 提交用户申请必填信息
           "submitMemberExtraInfo": "/sdk-web/v1/apply/submitMemberExtraInfo",  # 提交选填信息
           "triggerActivate": "/walletApp/activate/triggerActivate",  # 触发激活
            "user_setTransPassword":"/user/security/setTransPassword" ,  #设置交易密码
           "isSettedTransPassword": "/user/security/isSettedTransPassword",  # 用户是否设置支付密码
           "queryAgreement": "/sdk-web/v1/agreement/queryAgreement",  # 匹配资方获取协议二合一
           "verifyTransPasswordNew": "/user/security/verifyTransPasswordNew",  # 支付密码密码校验

           }

api_params = {
    "getPublicKey": {"timestamp": "1465802761723"},
    "user_login": {"mobilePhone": "", "verifyCode": "888888", "smsSerialNo": "2016061223292527",
                   "timestamp": "1465802761723"},
    "user_app_login": {"appId": "8bd5b7be4dd308ecd3be7e1cefd5246b", "deviceId": "C34E5462-1D8A-4885-9FCD-3D5942289522",
                       "mobilePhone": "", "password": "", "keyFlag": "", "timestamp": "1465802761723"},
    "user_publickey": None,
    "user_loginByPhone": {"phone": "", "verifyCode": "", "smsSerialNo": "", "timestamp": "1465802761723"},
    "sendPhoneVerifyCode": {"mobilePhone": "", "model": "200", "timestamp": "1465802761723"},  # 发送验证码
    "phoneLogin": {"loginType": "", "merchantId": "", "phone": "", "smsSerialNo": "", "storeId": "", "verifyCode": "", "timestamp": "1498113201940", "channelToken": "","merchantChannel": "",},  # 钱包动码登录
    "getApplicationInfo": {"timestamp": "1465802761723"},  # 获取App信息
    "getMobileNo": {"timestamp": "1465802761723"},  # 获取手机号
    "authorise": {"timestamp": "1465802761723"},  # 静默授权
    "submitMerchantOrder": {"applyTerm": "", "merchantOrderNo": "", "productId": "", "tdId": "", "timestamp": "1498122610798", },  # 创建钱包订单
    "submitApplyInfo1": {"accountInfo": "", "applyAmount": "",  "applyTerm": "", "createTime": "", "deviceInfo": "", "merchantId": "", "merchantOrderNo": "","mobileNo": "",
                        "productId": "", "productInfo": "", "productName": "", "receiptInfo": "", "repayType": "", "storeId": "", "timestamp": "1498122610798", "tradeInfo": "",},  # 预申请
    "submitApplyInfo": {"merchantOrderNo": "17022233573634669644","timestamp": "123", },  # 预申请
    "submitMemberInfo": {"timestamp": "1498113201940",},  # 提交用户申请必填信息
    "submitMemberExtraInfo": {"applyNo": "", "email": "", "qq": "", "timestamp": "1498122610798", },  # 提交选填信息
    "uploadEquipmentInfo": { "step": "", "timestamp": "1498113201940",},  # 上送设备信息
    "triggerActivate": {"timestamp": "1465802761723"},
    "user_setTransPassword": {"timestamp": "1465802761723", "password": "", "activateType": "100", "keyFlag": ""},
    "isSettedTransPassword": {"timestamp": "1465802761723"},  # 用户是否设置支付密码
    "queryAgreement": {"timestamp": "1465802761723"},  # 匹配资方获取协议二合一
    "verifyTransPasswordNew": {"timestamp": "1465802761723"},  # 支付密码密码校验
}

dubbo_api = {
    "caOrderResult": ("cn.memedai.cash.loan.facade.business.IDubboOrderBusiness", "caOrderResult", "1.0.0"),  #  审核通过接口


}
dubbo_api_types = {
    "caOrderResult": ["cn.memedai.cash.loan.facade.model.vo.CaResultVO"],  # 自定义的方法

}
if __name__ == '__main__':
    pass