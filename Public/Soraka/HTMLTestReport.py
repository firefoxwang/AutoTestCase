#-*- coding: utf-8 -*-
from xml.sax import saxutils
import re
import socket
import platform
import netifaces
__author__ = 'rudolf'
__version__ = "1.0.0"
class Template_rudlf(object):
    
    DEFAULT_TITLE = "Robot Framework Report"

    # html template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
    <link href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div id="div_base">

%(heading)s
%(teststatis)s
%(report)s
%(ending)s

</div>
</body>
</html>
"""
    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { white-space: pre-wrap;word-wrap: break-word; }

/* -- heading ---------------------------------------------------------------------- */
h1 {
	font-size: 16pt;
	color: gray;
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 2ex;
    margin-bottom: 3ex;
}

/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}

a.popup_link:hover {
    color: red;
}

.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;
    /* width: 500px;*/
}

}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 99%;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #74A474; }
.failClass  { background-color: #FDD283; }
.errorClass { background-color: #FF6600; }
.passCase   { color: #6c6; }
.failCase   { color: #FF6600; font-weight: bold; }
.errorCase  { color: #c00; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }


/* -- ending ---------------------------------------------------------------------- */
#ending {
}

#div_base {
            padding: 5px;
            width: auto;
            height: auto;
            margin: -15px 0 0 0;
}
</style>
"""
    HEADING_TMPL = """<div class='page-header'>
<h1>%(title)s</h1>
%(parameters)s
%(repotlog)s
%(failreason)s
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
""" # variables: (name, value)
    # ------------------------------------------------------------------------
    # Report
    #
    HEADING_LOG_REPORT = """<p class='attribute'><strong>%(name)s  :  </strong><a href="http://%(ip)s:8082/report/%(project)s.html"><strong>运行详情-- %(project)s</strong></a></p>
"""
    HEADING_Fail_Reason = """<p class='attribute'><strong>%(name)s :  </strong>%(reason)s </p>
"""


    TEST_STATIS_TMPL = u"""
<p>测试用例统计</p>
<table id='result_table' class="table table-bordered">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>用例总数</td>
    <td>通过用例数</td>
    <td>失败用例数</td>
    <td>通过率</td>
    <td>测试结果(是否允许发布UAT)</td>
</tr>
<tr id='total_row'>
    <td>%(test_count)s</td>
    <td>%(test_pass)s</td>
    <td>%(test_fail)s</td>
    <td>%(test_apr)s</td>
    <td>%(is_uat)s</td>
</tr>
</table>
<p>接口优先级别</p>
<table id='result_table' class="table table-bordered">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>接口总数</td>
    <td>1级通过率</td>
    <td>2级通过率</td>
    <td>3级通过率</td>
    <td>无级通过率</td>
    <td>接口通过率</td>
    <td>测试结果(是否允许发布UAT)</td>
</tr>
<tr id='total_row'>
    <td>%(count)s</td>
    <td>%(tag1)s</td>
    <td>%(tag2)s</td>
    <td>%(tag3)s</td>
    <td>%(tagn)s</td>
    <td>%(method_apr)s</td>
    <td>%(tag_uat)s</td>
</tr>
</table>


"""





    REPORT_TMPL = u"""
<p></p>
<p class='description'>总用例分布与执行情况</p>
<table id='result_table' class="table table-bordered">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>接口名称</td>
    <td>接口级别</td>
    <td>用例总数</td>
    <td>用例通过</td>
    <td>用例失败</td>
    <td>接口状态</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>总计</td>
    <td>%(method)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>&nbsp;</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = u"""
<tr>
    <td>%(name)s</td>
    <td>%(method_tag)s </td>
    <td>%(test_count)s</td>
    <td>%(test_Pass)s</td>
    <td>%(test_fail)s</td>
    <td>%(method_status)s </td>

</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)


    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)



    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

# -------------------- The end of the Template class -------------------


class HTMLTestReport(Template_rudlf):
    def __init__(self, stream, test_result, fail_type, title=None):
        self.stream = stream
        self.test_result = test_result
        self.method_count = 0
        self.test_count = 0 
        self.test_pass = 0
        self.test_fail = 0
        self.test_apr = 0
        self.tag1_p = 0
        self.tag1_f = 0 
        self.tag2_p = 0
        self.tag2_f = 0 
        self.tag3_p = 0
        self.tag3_f = 0 
        self.tagn_p = 0
        self.tagn_f = 0
        self.method_pass = 0
        self.method_apr = 0
        self.tag1_apr = '~'
        self.tag2_apr = '~'
        self.tag3_apr = '~'
        self.tagn_apr = '~'
        self.desc = None
        self.fail_reasons = []
        self.output = None
        self.fail_type = fail_type
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title

    def _generate_report(self):
        
        rows = []

        for k, v in self.test_result.iteritems():
            if 'desc' not in k and 'fail_reason' not in k:
                row = ''
                row = self.REPORT_CLASS_TMPL % dict(
                                        name=k,
                                        method_tag=v[0],
                                        test_count=str(v[1]),
                                        test_Pass=str(v[2]),
                                        test_fail=str(v[3]),
                                        method_status=str(v[4]),
                                        )
                
                self.test_count = self.test_count + v[1]
                self.test_pass  = self.test_pass + v[2]
                self.test_fail = self.test_fail + v[3]
                rows.append(row)
                if v[0] == '1' and v[4] =='PASS':
                    self.tag1_p = self.tag1_p+1
                    self.method_pass =self.method_pass+1
                elif v[0] == '1' and v[4] =='FAIL' :
                    self.tag1_f = self.tag1_p+1
                if v[0] == '2' and v[4] =='PASS':
                    self.tag2_p = self.tag2_p+1
                    self.method_pass =self.method_pass+1
                elif v[0] == '2' and v[4] =='FAIL':
                    self.tag2_f = self.tag2_f+1
                if v[0] == '3' and v[4] =='PASS':
                    self.tag3_p = self.tag3_p+1
                    self.method_pass =self.method_pass+1
                elif v[0] == '3' and v[4] =='FAIL':
                    self.tag3_f = self.tag3_f+1
                
                if  v[0] not in ('1','2','3') and v[4] =='PASS':
                    self.tagn_p = self.tagn_p+1
                    self.method_pass =self.method_pass+1
                elif  v[0] not in ('1','2','3') and v[4] =='FAIL':
                    self.tagn_f = self.tagn_f+1
                
            elif 'desc' in k:
                self.desc = v

            else:
                self.fail_reasons = v

        self.method_count = len(rows)
        
        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            method = str(self.method_count),
            count = str(self.test_count),
            Pass = str(self.test_pass),
            fail = str(self.test_fail),
        )
        return report
    
    def getReportAttributes(self):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        
        status = []
        
        if self.test_pass: status.append(u'通过 %s' % self.test_pass)
        if self.test_fail: status.append(u'失败 %s' % self.test_fail)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            (u'开始时间', self.desc[0]),
            (u'结束时间', self.desc[1]),
            (u'状态', status)
            ]
    def generateReport(self):
        report = self._generate_report()
        report_attrs = self.getReportAttributes()
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        ending = self._generate_ending()
        statis = self.__test_static()
        print statis
        self.output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            teststatis = statis,
            report = report,
            ending = ending,
        )
        self.stream.write(self.output.encode('utf8'))
    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL
    
    def __test_static(self):
        '''
        用例执行情况
        '''
        if self.test_count != 0:
            self.test_apr = int(round(float(self.test_pass) / self.test_count,2) * 100)
        if self.method_count != 0:
            self.method_apr = int(round(float(self.method_pass) / self.method_count,2) *100 )
        if (self.tag1_p+self.tag1_f) != 0 :
            self.tag1_apr = int(round(float(self.tag1_p)/(self.tag1_p+self.tag1_f),2)*100 )
        if (self.tag2_p+self.tag2_f) != 0 :
            self.tag2_apr = int(round(float(self.tag2_p)/(self.tag2_p+self.tag2_f),2)*100 )
        if (self.tag3_p+self.tag3_f) != 0 :
            self.tag3_apr = int(round(float(self.tag3_p)/(self.tag3_p+self.tag3_f),2)*100 )     
        if (self.tagn_p+self.tagn_f) != 0 :
            self.tagn_apr = int(round( float(self.tagn_p)/(self.tagn_p+self.tagn_f),2)*100 )  
        
        statis = self.TEST_STATIS_TMPL % dict (
            test_count = str(self.test_count),
            test_pass = str(self.test_pass),
            test_fail = str(self.test_fail),
            test_apr = str(self.test_apr)+"%",
            is_uat = 'OK' if self.test_apr >= 90 else 'NO' ,
            count = self.method_count,
            tag1 = str(self.tag1_apr)+"%",
            tag2 = str(self.tag2_apr)+"%",
            tag3 = str(self.tag3_apr)+"%",
            tagn = str(self.tagn_apr)+"%",
            method_apr = str(self.method_apr)+"%",
            tag_uat = 'OK' if (self.tag1_f == 0 or self.tag1_p =='~') and self.method_apr>=90  else 'NO'
            )
        return statis
    
    def _generate_ending(self):
        return self.ENDING_TMPL
    
    def _generate_heading(self, report_attrs):
        a_lines = []
        log_lins=[]

        failreason = []

        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        log_attrs = [(u'详细报告', self.title+"report"),(u'详细log', self.title+"log"), ]
        for name1 ,value1 in log_attrs:
            sysstr = platform.system()
            if sysstr == "Windows":
                print ("Call Windows email tasks")
                log_line = self.HEADING_LOG_REPORT % dict(
                        name=saxutils.escape(name1),
                        project=saxutils.escape(value1),
                        ip=socket.gethostbyname(socket.gethostname()),
                    )
                log_lins.append(log_line)
            elif sysstr == "Linux":
                print ("Call Linux email tasks")
                ip = netifaces.ifaddresses(netifaces.interfaces()[1])[2][0]['addr']  # 通过interfaces找到centos的第二个网卡名字
                log_line = self.HEADING_LOG_REPORT % dict(
                    name=saxutils.escape(name1),
                    project=saxutils.escape(value1),
                    ip=ip,  # ens192为内网ip网卡的名字 17.6.14配置在centos7的机器上 网卡名字比较奇葩
                )
                log_lins.append(log_line)
        fail_reason_count = {}
        for k, v in self.fail_type.iteritems():
            i = 1
            for v1 in v:
                for fail_reason in self.fail_reasons:
                    if re.search(v1, fail_reason, re.IGNORECASE):
                        fail_reason_count[k] = i
                        i = i+1
        reason_info = []
        if fail_reason_count:
            for key_reason, value_reason in fail_reason_count.iteritems():
                reason_info.append(key_reason + "--" + str(value_reason))
        else:
            reason_info = u"无错误信息"

        fail_attrs = [(u'错误原因汇总', ','.join(reason_info))]
        for name1 ,value1 in fail_attrs:
            reason_line = self.HEADING_Fail_Reason % dict(
                    name = saxutils.escape(name1),
                    reason = saxutils.escape(value1),
                )
            failreason.append(reason_line)


        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            repotlog=''.join(log_lins),
            failreason=''.join(failreason),
        )
        return heading
    def run(self):
        "Run the given test case or test suite."
        self.generateReport()
