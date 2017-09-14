# -*- coding:utf-8 -*-
'''
Created on 2016-12-2
'''

import jenkins

import HTMLTestReport
import RF_ENV
import RF_OUT_PARSE
import Send_Mail
import run_config
import sys
import os
working_path = os.path.realpath(__file__).split("Public")[0]
sys.path.append(working_path)
from Public.publiclibary import DB_Operation

reload(sys)
sys.setdefaultencoding('utf-8')


# 臨時增加方法

class AutoTestListen():
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, project_name):

        self.project_name = project_name

    def result_write_db(self, report_result, build_number, test_apr, jenkins_name, environment, test_count, test_pass,
                        test_fail):
        import json
        import time
        # 处理数据
        project_name = unicode(self.project_name, "utf-8")
        start_time_str = report_result["desc"][0]
        # print start_time[0:4]+"-"+start_time[4:6]+"-"+start_time[6:8]+" "+start_time.split()[1].split(".")[0]
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(
            start_time_str[0:4] + "-" + start_time_str[4:6] + "-" + start_time_str[6:8] + " " +
            start_time_str.split()[1].split(".")[0], "%Y-%m-%d %H:%M:%S"))
        end_time_str = report_result["desc"][1]
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(
            end_time_str[0:4] + "-" + end_time_str[4:6] + "-" + end_time_str[6:8] + " " +
            end_time_str.split()[1].split(".")[0], "%Y-%m-%d %H:%M:%S"))
        fail_reason = '&&'.join(report_result["fail_reason"]).replace("'", r"\'")
        project_name = project_name
        resut_json = json.dumps(report_result, ensure_ascii=False).replace("'", r"\'")
        insert_result_sql = " insert into autotest_result.report_result (project_name,resut_json,fail_reason,start_time,end_time,build_number,test_apr,jenkins_name,environment, test_count, test_pass, test_fail) " \
                            "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}', '{11}')".format(
            project_name, resut_json, fail_reason,
            start_time, end_time, build_number, test_apr, jenkins_name, environment, test_count, test_pass, test_fail)

        DB_Operation.DeUplinfo_By_Sql("wallet", insert_result_sql)


    def output_file(self, path):
        '''
                    文件输出后进行解析
        '''
        jenkins_config = run_config.jenkins_config  # 获取到jenkins配置
        server = jenkins.Jenkins(jenkins_config["jenkins_url"], username=jenkins_config['username'],
                                 password=jenkins_config["password"])
        jenkins_project_name = [i['name'] for i in server.get_jobs()]  # 列表解析出真实项目名字
        if self.project_name not in jenkins_project_name:  # 如果自动化用例的名字不在真实的项目名称中
            if self.project_name not in run_config.auto2jenkins:  # 自动化项目用例不在配置的项目里
                print "自动化用例项目名与用例项目不一致且未配置到run_config.py--->auto2jenkins"
                real_jenkins_project_name = 'Not configured to auto2jenkins'
                last_build_number = 'Unable to get'
            else:
                real_jenkins_project_name = run_config.auto2jenkins[self.project_name]
                last_build_number = server.get_job_info(real_jenkins_project_name)['lastCompletedBuild']['number']
        else:
            real_jenkins_project_name = self.project_name
            last_build_number = server.get_job_info(real_jenkins_project_name)['lastCompletedBuild']['number']
        if RF_ENV.get_env() is None:
            environment = 'sit'
        else:
            environment = RF_ENV.get_env()

        rop = RF_OUT_PARSE.RF_OUT_PARSE(path)

        filename = run_config.outputdir + "Robot Framework " + unicode(self.project_name, "utf-8") + ".html"
        try:
            fp = file(filename, "wb")
        except Exception, e:
            print Exception, ":", e

        out_result = rop.root_iter("suite")
        # 重新组合报告
        runner = HTMLTestReport.HTMLTestReport(stream=fp, test_result=rop.json_pro(out_result, ''),
                                               fail_type=run_config.fail_type, title=self.project_name)
        runner.run()
        if RF_ENV.jekins_remote() == 'jenkins' and (
                            runner.tag1_apr not in (100, '~') or runner.method_apr <= 99 or runner.test_apr <= 99):
            run_config.email_info["result"]['Subject'] = '[ALIUAT]' + '[' + self.project_name + ']' + \
                                                         run_config.email_info["result"]['Subject'] + str(
                runner.test_apr) + "%" if RF_ENV.get_env() == 'aliuat' else '[SIT]' + '[' + str(
                last_build_number) + ']' + '[' + self.project_name + ']' + \
                                                                            run_config.email_info["result"][
                                                                                'Subject'] + str(runner.test_apr) + "%"
            Send_Mail.send_email(run_config.send_info, run_config.email_info["result"],
                             run_config.project_mails[self.project_name] + run_config.ld_mails, runner.output,
                             run_config.send_annex)

        # 写数据库
        rop.auto_test["test_apr"] = str(runner.test_apr)

        self.result_write_db(out_result, build_number=last_build_number, test_apr=str(runner.test_apr),
                             jenkins_name=real_jenkins_project_name, environment=environment,
                             test_count=runner.test_count, test_pass=runner.test_pass,
                             test_fail=runner.test_fail)  # 写入数据库

