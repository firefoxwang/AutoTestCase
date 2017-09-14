# -*- coding:utf-8 -*-

from robotremoteserver import RobotRemoteServer
from DubboLib import DubboLibary

class MyRemote(DubboLibary):
    def __init__(self):
        DubboLibary.__init__(self)


if __name__ == '__main__':
    RobotRemoteServer(MyRemote(),host='192.168.1.1', port=8270, allow_remote_stop=False)
