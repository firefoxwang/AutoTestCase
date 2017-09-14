# -*- coding:utf-8 -*-
import platform

'''
Created on 2016-12-5

'''
# 自动化服务器测试报告放置的路径


sysstr = platform.system()
if sysstr == "Windows":
    print ("Call Windows tasks")
    send_annex = {"send_name": [],
                  "send_path": "C:\\AUTOTEST\\REPORT\\"}
    outputdir = "C:\\AUTOTEST\\REPORT\\"
    project_path = r"D:\\repo\\AutoTestCase\\"  # 本地或者winserver服务器上的运行目录 文件字母必须大写 否则可能被转义或者引号外加r防止转义
elif sysstr == "Linux":
    print ("Call Linux tasks")
    send_annex = {"send_name": [],
                  "send_path": u"/home/autotest/autotest/report/"}
    outputdir = u"/home/autotest/autotest/report/"
    project_path = u"/home/user/execution/"  # linux服务器上的运行目录

'''
配置各个项目的运行参数：
example :
wallet-sdk 项目名称
test_case : 测试用例集  , 若没有先后顺序 只需要写到用例集， 否则需要指定到 具体的 路径
include : 只执行 某一级别的用例
'''

project_config = [
    {"Test": {"test_case": [u"测试用例集"], "include": []}
     },

]

################ 配置发送邮件配置 ################


######### 发送邮件配置  ##############


project_mails = {

    "Test": ['youremail@qq.com'],

}

ld_mails = []

email_info = {'config': {"From": "自动化配置", "To": "测试以及相关人员", "Subject": "自动化测试配置异常--提醒"},
              'result': {"From": "自动化测试", "To": "测试以及相关人员", "Subject": "自动化测试报告 -- 通过率"}
              }

send_info = {"send_mail": 'autotest@qq.com', "send_pwd": "yoursercet",
             "send_host": "smtp.exmail.qq.com", "send_port": 25}

# 错误归类
fail_type = {u"Dubbo 服务异常": [u'Dubbo服务调用异常'], u'结果断言异常': [u"JSON查询结果比较"], u"测试脚本异常": [u"数据转换异常"],
             u"调用接口无返回值": [u"ValueError: No JSON object could be decoded"], u"关键字错误": [u"Keyword"]}

# jenkins相关
jenkins_config = {"jenkins_url": "http://yourjenkins.cn/", "username": "yourname",
                  "password": "yourtoken"}
auto2jenkins = { "test": "jenkinsname"}  # 建立自动化项目跟jenkins项目的对应关系
