# -*- coding:utf-8 -*-
'''
Created on 2016-9-2
'''
import json
import sys
import os
# 将自动化脚本目录添加到Python工作目录
working_path = os.path.realpath(__file__).split("Public")[0]
sys.path.append(working_path)
from robot import run
from robot.parsing import TestCaseFile
from robot.utils import ArgumentParser
from robot.errors import DataError, Information
import RF_ENV
from Send_Mail import send_email
# from __future__ import unicode_literals
from run_config import *
from AutoTestListen import AutoTestListen
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    '''
          传入项目名称:获取运行的参数
    
    '''
    # 获取环境参数并写入全局变量
    RF_ENV._init()
    if len(sys.argv) == 3:
        env = unicode(sys.argv[2], 'gb2312').lower()
        if env == 'aliuat':
           RF_ENV.set_env(env)
        elif env == 'jenkins':
            RF_ENV.set_jenkins(env)
        else:
            print('not correct environment')

    project_path = project_path + unicode(sys.argv[1], 'gb2312')
    prj = None  # 根据项目名称获取 运行参数
    run_tag = None  # 指定运行优先级
    for project_info in project_config:

        prj = project_info.get(unicode(sys.argv[1], 'gb2312'), None)
        if prj:
            if sysstr == "Windows":
                print ("Call Windows prj tasks")
                testcase_path = (project_path + u"\\" + i for i in prj["test_case"])
                run_tag = prj["include"]
                break
            elif sysstr == "Linux":
                print ("Call Linux prj tasks")
                testcase_path = (project_path + u"/" + i for i in prj["test_case"])
                run_tag = prj["include"]
                break
        else:
            continue
    if prj != None:
        if run_tag:
            if sysstr == "Windows":
                print ("Call Windows prj none tasks")
                run_script = u"run({0} ,outputdir=r'{1}\\',output='{2}output.xml', report='{2}report.html',log='{2}log.html',include={3},listener=AutoTestListen('{2}'))".format(
                    "u'" + "',u'".join(testcase_path) + "'", outputdir, unicode(sys.argv[1], 'gb2312'), str(run_tag))
            elif sysstr == "Linux":
                print ("Call Linux prj none tasks")
                run_script = u"run({0} ,outputdir=r'{1}/',output='{2}output.xml', report='{2}report.html',log='{2}log.html',include={3},listener=AutoTestListen('{2}'))".format(
                    "u'" + "',u'".join(testcase_path) + "'", outputdir, unicode(sys.argv[1], 'gb2312'), str(run_tag))
        else:
            if sysstr == "Windows":
                print ("Call Windows  prj none tasks")
                run_script = u"run({0} ,outputdir=r'{1}\\',output='{2}output.xml', report='{2}report.html',log='{2}log.html',listener=AutoTestListen('{2}'))".format(
                    "u'" + "',u'".join(testcase_path) + "'", outputdir, unicode(sys.argv[1], 'gb2312'))
            elif sysstr == "Linux":
                print ("Call Linux prj none tasks")
                run_script = u"run({0} ,outputdir=r'{1}/',output='{2}output.xml', report='{2}report.html',log='{2}log.html',listener=AutoTestListen('{2}'))".format(
                    "u'" + "',u'".join(testcase_path) + "'", outputdir, unicode(sys.argv[1], 'gb2312'))
        eval(run_script)
    else:

        email_content = '''{0} --- 项目没有配置运行参数,请及时配置！！！！ \n
配置方式 ：在路径 ./Public/publiclibary 下 配置 run_config.py 文件下的   project_config 数据。
配置各个项目的运行参数：
wallet-sdk 项目名称
test_case : 测试用例集  , 若没有先后顺序 只需要写到用例集， 否则需要指定到 具体的 路径
include : 只执行 某一级别的用例 。
现有配置 如下 :
'''.format(unicode(sys.argv[1], 'gb2312'))
        for i in project_config:
            email_content = email_content + "\n" + '{0}'.format(json.dumps(i, ensure_ascii=False, indent=4))
        send_email(send_info, email_info["config"], project_mails[sys.argv[1]], email_content)
