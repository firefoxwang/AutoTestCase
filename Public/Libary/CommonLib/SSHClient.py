#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
# 将自动化脚本目录添加到Python工作目录
working_path = os.path.realpath(__file__).split("Public")[0]
sys.path.append(working_path)
from Public.publiclibary.PublicData import *
from Public.Soraka import RF_ENV
import traceback
import paramiko



def SSHClient(server_type, command, env='sit'):
    """
    登录到远程服务器执行指定的命令，入参是命令字符串，返回是执行结果list
    :param server_type: 需要操作的服务器归属哪个系统，对应PublicData文件中server_connects中配置
    :param command: 要执行的命令，多条命令可使用英文分号; 分隔
    """
    try:
        if env.lower() == 'aliuat' or RF_ENV.get_env() == 'aliuat':
            print '已选择ALIUAT环境'
            server_info = server_connects['ALIUAT'][server_type]
        else:
            print '已选择SIT环境'
            server_info = server_connects['SIT'][server_type]
    except Exception as err:
        print('当前测试环境为【{0}】, 请检查Public\publiclibary\PublicData.py下是否配置【{1}】服务器连接信息'.format(RF_ENV.get_env(), server_type))
        print '\n'.join([str(err), traceback.format_exc()])
    #调用paramiko模块下的SSHClient()
    ssh = paramiko.SSHClient()
    #加上这句话不用担心选yes的问题，会自动选上（用ssh连接远程主机时，第一次连接时会提示是否继续进行远程连接，选择yes）
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #连接远程主机，SSH端口号为22
    ssh.connect(server_info[0], server_info[1], server_info[2], server_info[3])
    try:
        #执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        return stdout.readlines()
    except Exception as err:
        print '\n'.join([str(err), traceback.format_exc()])
    finally:
        ssh.close()

if __name__ == '__main__':
    pass
