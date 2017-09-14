# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from robot.api import logger
import os
import copy
import jpype
import json
import time
import traceback
import re
import RF_ENV
#from collections import Iterable, Mapping
from jpype import (JClass, JArray)
import platform
import sys

reload(sys)
sys.setdefaultencoding('utf8')


#jarpath="C:\AUTOTEST\workspace\AutoTestCase\PublicLibary\jars"
#jpype.startJVM("C:\\Program Files\\Java\\jre7\\bin\\server\\jvm.dll", "-Djava.ext.dirs=%s" % jarpath)

month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}


class DubboLibary(object):

    def __init__(self):
        sysstr = platform.system()
        if sysstr == "Windows":
            print ("Call Windows tasks")
            jarpath="C:\jars"  # win下路径是反斜杠
            #生产路径 ： C:\jars
            if not jpype.isJVMStarted():
                jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)
        elif sysstr == "Linux":
            print ("Call Linux tasks")
            jarpath = "/home/autotest/jars"  # linux下路径是斜杠
            if not jpype.isJVMStarted():
                jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)

        #定各个参数数据类型
        self.Boolean      = JClass("java.lang.Boolean")
        self.JObject      = JClass('java.lang.Object')
        self.JString      = JClass('java.lang.String')
        self.JMap         = JClass('java.util.Map')
        self.JHashMap     = JClass('java.util.HashMap')
        self.JList        = JClass('java.util.List')
        self.JArrayList   = JClass('java.util.ArrayList')
        self.JLong        = JClass('java.lang.Long')
        self.JInt         = JClass('java.lang.Integer')
        self.JDouble      = JClass('java.lang.Double')
        self.BigDecimal   = JClass('java.math.BigDecimal')
        self.Data         = JClass('java.util.Date')
        self.JStringArray = JArray(self.JString, 1)
        self.JObjectArray = JArray(self.JObject, 1)
        self.Parameter_type = []


    def __pytojavasign(self, obj):
        try:
            if isinstance(obj, int):
                return self.JLong(obj)

            elif isinstance(obj, long):
                return self.JLong(obj)

            elif isinstance(obj, float):
                return self.JDouble(obj)
            elif isinstance(obj, (str, unicode)):
                return obj
            elif isinstance(obj, dict):
                jmap = self.JHashMap()
                for key, value in obj.iteritems():
                    # 判断value是否 in (dict, list)
                    if isinstance(value, (dict, list)):
                        jmap.put(self.__pytojava(key), self.__pytojava(value))
                    else:
                        if isinstance(value, int):
                            value = long(value)  # linux上的需要修改成long类型
                        jmap.put(self.__pytojava(key), value)
                return jmap

            elif isinstance(obj, list):
                array = self.JArrayList()
                for item in obj:
                    array.add(self.__pytojava(item))
                return array
            else:
                return obj
        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            print 'Python->Java数据转换异常!'
            raise

    def __pytojava(self, obj):
        #Python 数据 类型转变为  Java 数据类型
        #使用递归函数
        try:
            if isinstance(obj, int):
                obj = long(obj)  # win下int会自动转换成long，但是linux下没有，所以还是都改成long，也许跟python版本有关系
                return self.JLong(obj)

            elif isinstance(obj, long):
                return self.JLong(obj)

            elif isinstance(obj, float):
                return self.JDouble(obj)

            elif isinstance(obj, (str, unicode)):
                if self.__judge_parameter_type():
                    return obj
                elif "{" in obj and "}" in obj[-1]:
                    return self.__pytojava(eval(obj))
                elif "[" in obj and "]" in obj[-1]:
                    return self.__pytojava(eval(obj))
                return obj
            elif isinstance(obj, dict):
                jmap=self.JHashMap()
                for key ,value in obj.iteritems():
                    #判断value是否 in (dict, list)
                    if isinstance(value, (dict, list)):
                        jmap.put(self.__pytojava(key),self.__pytojava(value))
                    else:
                        if isinstance(value, int):
                            value = long(value)  # linux上的需要修改成long类型
                        jmap.put(self.__pytojava(key),value)
                return jmap

            elif isinstance(obj, list):
                array = self.JArrayList()
                for item in obj:
                    array.add(self.__pytojava(item))
                return array

            else:
                return obj
        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            print 'Python->Java数据转换异常!'
            print repr(obj)
            raise

    def __javatopy(self, obj):
        # Java 数据类型修改为 Python 数据类型
        logger.info("将要进行javatopy转换的java对象格式为  {}".format(type(obj)))
        try:

            if isinstance(obj, self.JInt):
                return int(str(obj))

            elif isinstance(obj, self.JLong):
                return long(str(obj))

            elif isinstance(obj, (self.JDouble,self.BigDecimal)):
                return float(str(obj))
            elif isinstance(obj, self.JObjectArray):
                lst = []
                for i in range(obj.length):
                    iv = self.__javatopy(obj[i])
                    lst.append(iv)
                return lst
            elif isinstance(obj, self.JStringArray):
                lst = []
                for i in range(len(obj)):
                    iv = self.__javatopy(obj[i])
                    lst.append(iv)
                return lst
            elif isinstance(obj, self.JList):
                lst = []
                for i in range(obj.size()):
                    iv = self.__javatopy(obj.get(i))
                    lst.append(iv)
                return lst

            elif isinstance(obj, self.JMap):
                dic = {}

                for k in list(obj.keySet().toArray()):
                    # logger.info("type(obj.keySet().toArray() {}".format(type(obj.keySet().toArray())))
                    if isinstance(k, self.JInt):
                        dic[str(k)] = self.__javatopy(obj.get(k))
                    else:
                        # logger.info ("obj.get(k), self.__javatopy(obj.get(k))\n {0},{1}".format(obj.get(k), self.__javatopy(obj.get(k))))
                        dic[k] = self.__javatopy(obj.get(k))
                return dic
            elif isinstance(obj, self.Data):
                b = re.match(r'^\d{4}[-]([0][1-9]|(1[0-2]))[-]([1-9]|([012]\d)|(3[01]))', str(obj))
                if b:
                    return str(obj)
                else:
                    a = str(obj).split(' ')
                    return(str('{0}-{1}-{2} {3}'.format(a[-1],month[a[1]],a[2],a[3])))
            elif isinstance(obj, (str, unicode)):
                if obj == '':
                    return str(obj)
                elif "{" in obj[0] and "}" in obj[-1]:
                    return eval(obj.replace(": true,", ": \"true\",").replace(": false,", ": \"false\","))
                    # 解决带过来的字符串包裹的字典里的java true到python True的问题
                elif "[" in obj[0] and "]" in obj[-1]:
                    return eval(obj.replace(": true,", ": \"true\",").replace(": false,", ": \"false\","))
                else:
                    return obj
            # elif isinstance(obj, self.Boolean):  # 针对传过来的是java的true，转换成布尔类型
            #     return bool(obj)

            else:
                return str(obj)
        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            print 'Java->Python数据转换异常!'
            print obj
            raise

    def __javatopy_new(self,obj):
        # Java 数据类型修改为 Python 数据类型
        # 适配Map_To_Sign_New
        try:

            if isinstance(obj, self.JInt):
                return int(str(obj))

            elif isinstance(obj, self.JLong):
                return long(str(obj))

            elif isinstance(obj, (self.JDouble,self.BigDecimal)):
                return float(str(obj))
            elif isinstance(obj, self.JObjectArray):
                lst = []
                for i in range(obj.length):
                    iv = self.__javatopy_new(obj[i])
                    lst.append(iv)
                return lst
            elif isinstance(obj, self.JStringArray):
                lst = []
                for i in range(len(obj)):
                    iv = self.__javatopy_new(obj[i])
                    lst.append(iv)
                return lst
            elif isinstance(obj, self.JList):
                lst = []
                for i in range(obj.size()):
                    iv = self.__javatopy_new(obj.get(i))
                    lst.append(iv)
                return lst

            elif isinstance(obj, self.JMap):
                dic = {}
                for k in list(obj.keySet().toArray()):
                    print k, obj.get(k)
                    dic[k] = self.__javatopy_new(obj.get(k))
                return dic
            elif isinstance(obj, self.Data):
                b = re.match(r'^\d{4}[-]([0][1-9]|(1[0-2]))[-]([1-9]|([012]\d)|(3[01]))', str(obj))
                if b:
                    return str(obj)
                else:
                    a = str(obj).split(' ')
                    return(str('{0}-{1}-{2} {3}'.format(a[-1],month[a[1]],a[2],a[3])))
            elif isinstance(obj, (str, unicode)):
                if obj == '':
                    return str(obj)
                else:
                    return obj
            else:
                return str(obj)
        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            print 'Java->Python数据转换异常!'
            print obj
            raise

    def __judge_parameter_type(self):
        if self.Parameter_type:
            if len(self.Parameter_type) == 1 and 'java.lang.String' == self.Parameter_type[0]:
                return True
            else:
                return False
        else:
            return False

    def __shutdownJVM(self):
        jpype.shutdownJVM()

    def __pytomap(self,obj):
        if isinstance(obj, dict):
            return obj
        else:
            return eval(obj)

    def __pytolist(self,obj):
        #该转换 只是 类似于 "[]"的字符串 进行转换 成 list
        if isinstance(obj, list):
            return obj
        else:
            print obj
            return eval(obj)

    def Map_To_Sign(self,params):
        '''
        aptosign 对map 进行数字签名，\n
                    返回签名后的map \n
        Example : \n
        | ${x}= | maptosign | mapinfo | \n"
        '''

        self._result=""
        try:
            self.SignMap=jpype.JClass("com.mime.qa.robotframework.creditwallet.walletkeyword.SignMap")

            sm = self.SignMap()
            if isinstance(params,str):
                params = eval(params)
                result=sm.maptosign(self.__pytojavasign(params))
                self._result = str(self.__javatopy(result))
            else:
                result=sm.maptosign(self.__pytojavasign(params))
                self._result = self.__javatopy(result)

        except Exception, e:
            print '调用jar 包异常'
            print e
        return self._result



    def connect_to_dubbo_register(self, zkUrl):
        """连接到Dubbo注册中心

        参数zkUrl是注册中心地址，例如zookeeper://99.48.66.13:2181

        Example:
        | Connect To Dubbo Register | ${zkUrl} |
        """
        if RF_ENV.get_env() == 'aliuat':
            zkUrl = 'zookeeper://192.168.10.6:2181'
            print('dubbo环境切换为{0}, {1}'.format(RF_ENV.get_env(), zkUrl))
        self.DubboClient=JClass("com.mime.qa.dubbo.DubboClient")
        self._dubbo_client = self.DubboClient(zkUrl)
        print 'self._dubbo_client ', self._dubbo_client
        self._result = None  # 尝试retrun一下看能不能改变返回值



    def call_dubbo_interface_method(self, interface_name, method_name, parameter_types,interface_version=None,*args):
    # def call_dubbo_interface_method(self):
        """调用Dubbo接口方法

        interface_name：接口名，例如cn.memedai.menotification.push.service.PushMessageService
        method_name: 方法名，例如pushToSingle
        parameter_types：参数类型数组, 例如['java.lang.String', 'cn.memedai.menotification.push.bean.Message', 'cn.memedai.menotification.push.bean.PushTarget', 'cn.memedai.menotification.push.bean.PushConfig']
        args：参数数组，例如['哈哈', msg, pushTarget, None]
        pre_process : 预处理器, 当数据不满足要求是 ，自己进行处理
        parameter_types和args的顺序必须保持一致，基本类型直接写，POJO需转成字典

        Example:
        | Call Dubbo Interface Method | ${interface_name} | ${method_name} | ${parameter_type} | ${datax} | ${interface_version} |
        """
        try:
            if parameter_types is not None:
                self.Parameter_type = parameter_types
                parameter_types = self.JStringArray(self.__pytolist(parameter_types))
            print("传入dubbo接口的入參为 {}".format(args))
            # _args = self.__pytojava(([self.__pytojava(o) for o in args]))
            args_real = []
            for k in args:
                if k is not None and k != "" and isinstance(k, (str, unicode)):
                    if "'" in k[0] and "'" in k[-1]:  # 解决入参是字符串样子的字典问题
                        k = k.strip("'")
                    else:
                        if "{" in k[0] and "}" in k[-1]:
                            k = eval(k)
                        elif "[" in k[0] and "]" in k[-1]:
                            k = eval(k)
                if k == "null":
                    k = None
                args_real.append(k)
            _args = self.__str_to_jsonObj(tuple(args_real))
            print("Dubbo接口入参为  {0}".format(_args))

            # print("pytojava转换后的入参为  {0}".format(_args))

            result = self._dubbo_client.invoke(interface_name, interface_version, method_name, parameter_types, _args)

            print("Dubbo返回的出参为 {}".format(result))
            # self._result = self.__javatopy(result)
            self._result = self.__jsonObj_to_str(result)
            if self._result == 'None':
                # 抛出自定义异常
                raise Exception("Result is none,please check  parameters ")

            print("出参经过jsondumps转换后的漂亮json格式为:\n{0}".format(json.dumps(json.loads(self._result), ensure_ascii=False, indent=4)))

        except Exception, e:
            print 'Dubbo服务调用异常'
            print traceback.format_exc()
            raise e

        return self._result

    def dubbo_interface_mock(self, interface_name, expect_result):
        self._dubbo_client.mock(interface_name, self.__pytojava(expect_result))


    def __jsonObj_to_str(self,map):
        Object  = JClass("com.mime.qa.dubbo.JsonUtil")
        json_str = Object.toJSONString(map)
        return json_str

    def __str_to_jsonObj(self,str):
        Object = JClass("com.alibaba.fastjson.JSON")
        json_str = json.dumps(str)
        jsonObj = Object.parse(json_str)
        return jsonObj






if __name__ == '__main__':
    pass
