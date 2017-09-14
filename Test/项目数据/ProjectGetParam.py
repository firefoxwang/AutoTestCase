# -*- coding:utf-8 -*-
# from __future__ import unicode_literals
from bpmappers import Mapper, RawField, ListDelegateField
from ProjectData import *
from robot.api import logger

'''
Created on 2016-8-11

@author: Rudolf Han
'''


#
# wallet_params={'login':{'phone': '13621780941', 'verifyCode': '888888', 'timestamp': '1465802761723', 'smsSerialNo': '2016061223292527'},
#               'submitbasice':{}}

def to_json_param(api_name, *params):
    # 根据类获取接口 定义的基础的参数
    base_param = api_params[api_name]
    if params:
        for param in params:
            # print param.split("=")[0],param.split("=")[1]
            if param.split("=")[1] == 'None':
                base_param[param.split("=")[0]] = ''
            # elif "[" in param.split("=")[1] and "]" in param.split("=")[1]:
            #                base_param[param.split("=")[0]]=eval(param.split("=")[1])
            else:
                base_param[param.split("=")[0]] = param.split("=")[1]
    # 定义最终输入的参数
    param_json = {}

    if base_param != None:
        for key in base_param:
            param_json[key] = RawField()

    else:
        return None

    ##动态生成  类 并且 通过bpmappers 生成 json
    MyShinyClass = type('MyShinyClass', (), base_param)
    # FooChild = type('FooChild', (Mapper,), {'phone': RawField()})
    FooChild = type('FooChild', (Mapper,), param_json)

    FooChild(MyShinyClass).as_dict()

    return FooChild(MyShinyClass).as_dict()


def get_post_url(api_name):
    try:
        if 'user_' in api_name:

            post_url = api_host + api_url[api_name]

        else:
            post_url = api_host + api_url[api_name]

        return post_url

    except Exception, e:

        logger.info(u"不存在接口名:{0}对应的 url ,原因为 ：{1}".format(api_name, e))


def get_post_heards(api_name, heads_info=None):
    try:
        if 'user_app' in api_name:

            heards_json = heard_info_app

        else:

            heards_json = heard_info_app

    except Exception, e:

        logger.info(u"不存在接口名:{0}对应的 heards ,原因为 ：{1}".format(api_name, e))

    return heards_json


def split_equal_value(value, split_value="="):
    value_info = value.split(split_value)[1]

    return value_info


def get_dubbo_method(api_name):
    try:
        base_param = dubbo_api[api_name]
        class_name = base_param[0]
        method_name = base_param[1]
        dubbo_version = base_param[2]
        parameter_types = dubbo_api_types[api_name]
        return class_name, method_name, dubbo_version, parameter_types
    except Exception, e:
        logger.info(u"不存在接口名:{0}对应的  class_name,method_name,请检查ProjectData.py 是否已经配置 ".format(api_name))





