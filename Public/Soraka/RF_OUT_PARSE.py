# -*- coding:utf-8 -*-
'''
Created on 2016-12-7
'''
#from bs4 import BeautifulSoup
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class RF_OUT_PARSE():
    def __init__(self,path):
        
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.auto_test = {}
        self.auto_result = {}
        self.fail_reason = []
        self.content = open(path, 'r').read()
    def json_pro(self, v, k=''):
        for k1, v1 in v.iteritems():
            if isinstance(v1, dict):
                self.json_pro(v1, k1)
            else:
                self.auto_result[k+"."+k1] = v1
        return self.auto_result
    def root_iter(self,tag):
        #soup = BeautifulSoup(self.content, 'lxml')   #用bs4的方法载入整个xml
        #bs4_tag = soup.find('statistics')
        #all_test = bs4_tag.find('stat', text='All Tests')
       # test_fall = int(all_test['fail'])
        #test_success = int(all_test['pass'])
        #test_total = test_fall + test_success

        for i in self.root.iter(tag):

            def child_xpath(elem, _tag):
                suit_info = {}

                for j in elem:
                    test_info = []
                    tag = '未设置' # 定义级别tag= 1 接口数据
                    test_count = 0 #接口下的用例
                    method_status = '' #是否成功
                    test_count_pass = 0 #通过
                    test_count_fail = 0 #失败

                    if j.tag == 'test':   # j为生成的xml，最大的suite
                        for jj in j:      # jj是指s1-s1-t1,t2,t3
                            if jj.tag == 'tags':
                                '统计  tag 个级别数据'
                                tag = jj.find('tag').text
                            if jj.tag == 'status':
                                if jj.attrib["status"] == u'FAIL':
                                    test_count_fail = test_count_fail + 1
                                    self.fail_reason.append(jj.text)
                            if jj.tag == 'status':
                                if jj.attrib["status"] == 'PASS':
                                    test_count_pass = test_count_pass+1
                                test_count = test_count + 1
                            if jj.tag == 'status':
                                method_status = jj.attrib["status"]
                        test_info.append(tag)
                        test_info.append(test_count)
                        test_info.append(test_count_pass)
                        test_info.append(test_count_fail)
                        test_info.append(method_status)
                        suit_info[j.attrib['name']] = test_info
                        child_xpath(j,_tag+"."+j.tag,)
                return suit_info

            cx = child_xpath(i,i.tag)
            if 'name' in i.attrib.keys():
                self.auto_test[i.attrib["name"]] = cx
        self.auto_test['desc'] = [self.root.find("suite/status").attrib['starttime'],self.root.find("suite/status").attrib['endtime']]
        self.auto_test['fail_reason'] = self.fail_reason
        return self.auto_test

# rop = RF_OUT_PARSE(u"F:\\REPORT\\资方管理系统output.xml")
# print rop.root_iter("suite")
#解析结果数据 ：  1.1资方匹配接口(模块) --{模块:{接口名:[],接口名:[接口运行结果]}}
