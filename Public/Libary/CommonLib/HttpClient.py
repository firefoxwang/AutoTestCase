# -*- coding:utf-8 -*-
'''
requests 类的在封装，进行访问 http 请求

'''
from __future__ import unicode_literals

from robot.api import logger

import requests

import json

from poster.encode import *

from poster.streaminghttp import *

import urllib2
import traceback
from requests import post
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

__version__='1.0.0'

__author__='rundof han'

class HttpClient:
    
    #初始化 
    def __init__(self):
        #'content-type': 'application/json',
        self.isSession=True
        self.jason_info=''
        self.cookie_info=''
        
        self.is_session = self.isSession 
        if self.is_session:
            self._sobj = requests.Session()
        self.resp = None
    # get请求，返回的是对象    
    def http_get(self,url,heard_info,param=None,time_data=30):

        try:
            logger.info("请求URL链接为:\n\n{0},\n请求体为：\n\n{1}".format(url,json.dumps(param,ensure_ascii=False,indent=4)))
            if param:
                param=eval(param)
            self.resp = self._sobj.get(url,headers=heard_info, params=param,verify=False,timeout=time_data,allow_redirects=False)
            # 对返回状态非200状态直接抛异常
            if self.resp.status_code != 200:
                raise Exception(self.resp)
        except Exception , e:
            raise e
            # print e
            # self.resp=None
        return self.resp
    #post 请求 ，返回的是对象    
    def http_post(self,url,heard_info,param=None,files=None,time_data=30):
        """ Send a POST request 

        `url` to send the POST request to

        `param` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content

        `heard_info` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to POST to the server
        
        `time_data` connection timeout
        """

        try:
            logger.info("请求URL链接为:\n\n{0}".format(url))
            logger.info("请求体为：\n\n{0}".format(json.dumps(param,ensure_ascii=False,indent=4)))
            if param and heard_info.has_key('Content-Type') and heard_info['Content-Type']!='application/x-www-form-urlencoded': #短路规则
                param=json.dumps(param)

            self.resp = requests.post(url,headers=heard_info,data=param,files=files,verify=False,timeout=time_data,allow_redirects=False)
            # 对返回状态非200状态直接抛异常
            if self.resp.status_code != 200:
                raise Exception(self.resp)
        except Exception , e:
            raise e
            # print e
            # self.resp=None
        return self.resp
    
    def upload_file(self,url,mmticket,file_name):
        register_openers()
        files = {"header": open(file_name,"rb"),"filename":"header.png","type":"1"}
        datagen, headers = multipart_encode(files,"311369e5-530f-4e91-b240-cef8a82eb7c5")
        headers["mmTicket"]=mmticket
        headers['Accept'] = '*/*'
        headers['uuid'] = 'C712929A-4A9A-4D85-AD2E-A84538C547CD'
        headers['MPTSP'] = '1480402744000'
        headers['clientid'] = '35b0c99587840a77205883d96723b18a'
        headers['sysVersion'] = '1.4.3'
        headers['merchant_id'] = 'MEIYA'
        headers['channel'] = 'iOS'
        headers['accept-language'] = 'zh-Hans-CN;q=1'
        print('headers:'+str(headers))
        try:
            logger.info("请求URL链接为:\n{0}".format(url))
            request = urllib2.Request(url, datagen, headers)
            respon_info=json.loads(urllib2.urlopen(request).read())
            logger.info("返回数据:\n\n{0}".format(json.dumps(respon_info,ensure_ascii=False,indent=4)))
            return respon_info
        except Exception,e:
            print e
            return None

    def upload_file_ocr(self,url,mmticket,files):
        """
                    上传图片 
        `url` to send the POST request to
        'mmticket' token
        'files' 文件流
        """
        # 在 urllib2 上注册 http 流处理句柄
        register_openers()

        # 开始对文件 "*.jpg" 的 multiart/form-data 编码
        # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置

        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        #{"uploadFile": open("F:\image\zm.jpg", "rb"),"filename":"zm.jpg","type":"1"}
        datagen, headers = multipart_encode(files,"----------WebKitFormBoundaryt266N78rSLurB45U")

        headers["mmTicket"]=mmticket
        # 创建请求对象
        
        try:
            logger.info("请求URL链接为:\n{0}".format(url))
            request = urllib2.Request(url, datagen, headers)
            respon_info=json.loads(urllib2.urlopen(request).read())
            # 实际执行请求并取得返回
            logger.info("返回数据:\n\n{0}".format(json.dumps(respon_info,ensure_ascii=False,indent=4)))
            return respon_info
        except Exception,e:
            print e
            return None


    def to_json_data(self,pro):
        json_info=''
        try:
            json_info=pro.json()
            logger.info("返回结果为：\n{0}".format(json.dumps(json_info,ensure_ascii=False,indent=4)))
        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            json_info="unkonow json data"
        return json_info

    def to_content_data(self,pro):
        content_info=''
        try:
            content_info=pro.text
        except:
            content_info="unkonow json data"
        return content_info

    def sso_login(self,url):
        jSessionId = None
        heard_info = {'Content-Type': 'application/x-www-form-urlencoded',} # form表单提交
        body_for_cta = "username=zby%40mi-me.com&password=111111&lt=LT-31710-bpubpC6GPD2dqnbiMqGJUKZ15A0ioO-cas01.example.org&execution=169de5c4-5076-4c0a-aef5-53e56e9c6370_AAAAIgAAABCJh7CaUa5v3rZjtLQBuP8VAAAABmFlczEyOEAbygr%2BZ0HOTwVVf%2BSLmzsyEqeLd2pH6IQ9Qtphk6%2B11YOiTFXYAbNeDis0JOzzBoluqTBRuAi8czzmOa1ba7A40Pc7jhh5kGXwGqFW8nwdBNaZ9eqDePDpb66xS22VbkeLWTZYdMNFhnUSHQtww6u5pEumZjbw25hU9ot7Immn9KhI1wfQZe2gLL5jolBKb71AIlO%2BsUDp3dKk91TUl0qjKM7UjFS0yHY2YhNQePfYIl18SmubLCar6en6Dx5vn8yhGFTSZbddyphGh2nUl9R7bDhbs3%2FWfPUJW5zq4o0Zy8PJ3aClCcty2lpK6XTc7oHHiGnD20%2BSc%2FBwfXlRPxInmdrA3K72te3QeYaLxCzjAWSm1Ve%2BTsPCF3lBspXgb8I5hOjHZYk%2F98l7ej0BPb7UEk2OK56mc67nbZSf1FAn5pho0ybxZ%2FoCVihYYVE8ck1GJnFdR%2FNF%2FVlzNjor2xpw3TpaRpE0BCBJsHRIorw%2FWij0hRWJCIVPBgamDZALy03%2BFAv72CmZuC88duf2Am4XULVsVANt%2FVN4fr0WQAJfHbO1TS4AuXjk4qoLmLEPLfI6lu%2B72%2ByltnG6oCIpZY6HNTRDcT1dZPw%2FJDGIyy9upqvjSmyZs9jvC0ckpc1n0F3WyN9nHEm%2BhMtlZ0VW%2F8NivZy4cyRnXrpVKaNwbVHySd3CYqNKK21yRWT7Q1XTUqayQ0vtGai8pRz9ZiKToiTz%2F5Jes7ZC63U9ITpiB3L0V%2BnQm7XqcskmnHTpVxfDrnRDtYpflQWMNpD2laDUpnKMy588hfzcgIhspQ%2Ff6YhSaFmyXJNUy%2FM6uRZGdcdSekP1%2Fw%2FQhC2ZNyKLWbJsHrwW3pfIw5aZRfYVreiTQ%2F0j9XUQ8vlrPo3w35aK1or7A1HZDVcPYIByP9iaOtVuwBcpUfF2AtU2yUIRColvSHDHyl%2Bq9h1ApD%2BsTCUaiWwM8xgKZfJ%2F5uuTHiG4QGonpijvg7wxB%2BA6nvwHcO%2BdHEudAF9NFar5EQDeEWN0%2FlszbjxwBG69ef1%2FKcjnsMyziv0mZQl74NpFD%2BhyYo%2Fc6madX%2B7FwlhUdC4cBxD04wW1pv9OrEgj0j9NHsUZ3e7FM3ksH8%2F5AGr4xzbHpwopqjVQ8m9hCMWT3a1vWtwIC67ZMFwdhoRlHZ%2FOW6NRjrN81WxhAuP%2FcncGrrtTkdNq258WncW7J1UvEEV311bqkK1PCFex7%2BcDaSl98pVwWKD3paMyzw6%2BBbt6TbjEd7AjFLBEs2pYgArUT5uKINBJSufzraokqtaU68F5ErWL%2Fd7r9fhWQ7OhX%2BlGjg6jtU4z1aUsDBETp8O4SyfmKoI%2BS52LfyEMdR5FeU7m9iK4L1nBWQgn7Bu4dBjjSyxhFQzBjZ%2Bv0SDs7JrQ5f402zdc8WK31wK%2FQYZPNdpH83E1NxemGWiIgNoqLQlrNuCjOG%2F5sj3G1P35%2FO%2BXDFg5LRbLc%2FmO7p9NxwwX1TlXpx%2Bl5b06g64q7Vjk0iw1qfvTSNdpIGyRPeuQaga1U1pV0OOsbcgCyNv0M%2FQq4p4EklCE33a6e1EbFUhlcClWqG8uaEks57%2BkgkTtwT20PqAe0dbMBQ1RqbkDBu%2Brw%2FmtNmEYiHfthagDnN9Koz3ARGOybPeEoX8kUOC1G2m%2Bu8BEEg1c9zKVCguiE5yQrbuajBlrEaJF%2FtLzRtsjsR8vOISqAXlWwCPuc51X2uou%2Fv2wN9f7cT%2B8ie8kexEodBbXjO2%2BR0dGHXESo32oj3PD3%2BXERbH08enwaNaLp7ReOSqgIs%2ByH%2FjSL%2FiVvHyUFtq3gxmYv%2FhtbswrwntQ5lTsQKsBW%2FCa7DuWyEXHj7G3ly7SqVjdkElXJ0RFaQ5N5MC9PPjvhqIwkM%2F4JiBnFDmvbKyiy8OX69HJlyt5oVwBGTFYEGijgQIFJrcCuSWC6ho298MyMjncAJq9Or8xehMAeYtkqNYg1Rwxwo2ptVQfCBwAEQKjFWt8Lqg06rqRvflywuSS58Dqo3nAI0%2B9gQ%2BvjS9idbxFgquj1EXgtBe3xZhr8AdRCA%2FjV%2Bcdzxkgdtm2ZhC5OTxOMVk811nL4pMc%2BRUrTPgDjXrSL6cEXpxR7HcbmNJc6yq2Vkrh2KUs%2FaGEwJa4QVOlLpiSULCLcrLVWiaT4n%2Fc060xzMIuruFihelsjWibglLQ%2FI8hdVk8gZRqoDiYjg43BnAY6CL%2BchuKq813fiJa3z0hsg7Skv4tiUCO9WSLLm4fl2gH2QfYmRiVgqQ7gbnVRaOKuR11ZO9v6ih0x2bxz0ejALikxpShRP22VH3LCRQh5lbjtIJSmHIFcf78FnMruNroBNNv7pbNPXFlRstW3wVDG7h0XyONynatVdFj3TMDqE9iTeDs32kMEAfqG3B7IYkwM7gsOLl8KYOh2QIZ5tbFgtIGwJR%2B552uD1i%2B2z6SjBoei7xPzCccoZRdfg96b7IqYkKovxb88dJo3a4Vkj6%2F&_eventId=submit&submit=%E7%99%BB%E5%BD%95"
        body_for_coupon = "username=zby%40mi-me.com&password=111111&lt=LT-200-fyxCe4ogj1MyRyf1Ns1fPOJs3zjYN7-cas01.example.org&execution=9666dbbe-0d58-42bb-83f5-fc64337769e9_AAAAIgAAABB5fgGXM6R6lD%2fOepZuV0DQAAAABmFlczEyODYS0Rw6KXqj1UPBxq5qM8BnSC7%2fFz9YWrCPLyZQ%2bk9f7aqJ7GNjne8Z%2bJwAGvVqQIs3dELe1TEqG%2bvbtijqdIZga9uDq7LLKSmJVcaB30FpBXiRwMua7BZsUPUZsewNXxOvtnwY01mNRZl6akXCZsUMP0GOe4w7zQEbZPJPgudaC0j6Se0kKZFVHY3GLaNbmW57DR1ZSPlCwNv0A%2f8tYUoTLC3%2b5VCTI6Tx%2fzqXvgCIjtms1Z6CwUqz1Ov2t03CoxkICxEi1gz1eNvzwmwwgPXvsJgWd%2biHtttkbXNxUiefxKxaJAYq%2ftJcm3d0Ltswkpr2YwKRFjCzHTFh2haB%2f2F5KMRjUFs63MRfhzkP%2f8fPGlf93q%2fk54KVL4%2b%2f4vqWf6IoGQnQMjPp7AvJ3mbUWwJOUPxnFgMqCf3TGYG3Y0AWCIQGUyyQeCqlEbjuR%2bCbWm64xCtEFsYZTPcAx%2f25X1SI5uzdvhCZUGa3seikcGMIWXKI15PxloTqgiXWFqLxxVFqRQy9Dhv%2feRydXQjwZZyUOzA6DMIYLzWE5WIR%2bYEAbF4kjcmcE4asFeEHKcUU7i5qC5XqGs0I77EpfnSwQujJIHluwKJEG1oe%2bQ1jWYztFyuE0Iy2TnIwoglYqNuGyze%2b%2bnZvWtdBY8omDE0nTwDGthYxDaWPf674%2bJY00fU3EqAl9mGclH8MLwDpWo9eX5dZR%2b%2bK908u8bnoozvNp4nWeF%2fBwHvyKZzUn5ld%2b3obhg7%2f8eQx03G9amKFivGdbg4PDdN05vJBNBFr1zRxMO2FV9kfISfkDoCTNAtbd34H%2fvQMkuZtKHltQvsXITmfk6%2bKNlD61GsaifI%2fIA96KKiuB0rtddYLhz8oVknz2Mbb7Ue%2bGyT146mV96gXTAyisRtoBGADzh7GyTai9Ohxk5mfUeYfHCIg3ISF7pr%2fZCQoaVIEkKzqJDWa2%2bNXsrAbmduJLxh%2btGoB9RakRIeR9JNSoQi2CnmH55hmryZ3r%2b%2bfXwnA6nMUur8dkuer%2f%2fhH87oMH8yCkjGkB3iemm1JK2NqFY2wiDI%2fBK3IUW16BQ%2flKGfZ1sMfqz1TenVIdrJbqKd6KGg6SdPcU2aLUVU%2bNmqRN13oLEMJPRQDihmob0lt8rtFygJfnBUeu1YYKaPbR%2bC2%2bH3xRQASLt9QrRBvG7XltOQD1N%2bfmKPuAnqf7U7cqJcM8D7t1Dc9zZX8GfL9BxJq5E%2bXFK0m17J08lipH3MEdqRkRPRVoe8BrxV9JZ8XPil3P5X%2fomge%2boXGEOj6VgAU%2brfcl8QVIFxrBr8GEEmqBfV1gIOyyBOX9DUJzO0WHhMrxfS7CqSagu9VaHlztXhJneyc8t0uDFAq5i7XTmg2hIwNCSxgfzzerxj6UmpWdT8xCMjt94KP%2bW8UDTMLL%2brT%2ffQn9QLfESooPoKMbe%2bdFjsJlhCg72DfA9OVPECQ7iINBxS912McU3sNq%2bes3F17ooqDISVy%2bRMHMCSAaP4LKeZk9%2ffqiqrY6avqzMH7YKf98KxKSn5kUoKzSyEXpA7jkp%2bt4sRS%2buGC%2bh88gp%2fB%2bwTNPZzjvDAeyliDeFSzbVTKlC5FGN8b7CJ63y%2fSZso6HVijfJqknYCzcLtCml4zYF8aiDT2TWFwcz15Bk1H3h5vaT%2bexGtvfLZ3xmlwHg5WPkmgxMMosSxuV1zCY1Qewc5vKggWjrXDM0fbsmHYPTmxZCUme1ynm5PppY74Nk7jwr792sZdma3wLicZsCul8lJp2o%2bGgGeBRUKtS7vlCIkkvsePSnHqCYCr7d80K0xjd6NPl3F1FjrR7KJPmf3313T8%2bLtuqtoiIGJUvoh9Ku6E4q7DkG5%2bZoAqv1tq1r%2fcQL1CxMS6FMYrBKmEzjHDkxg3hPXdqmwpoH6Fw45XVIKka7lPaWRiQNyCwmM%2f%2f5WahwBJrd2qXPKbgdrByhiH7Y3BFW8Jub263EQ1T0nkb%2fOjRFbyCZDW3jX8oxw0GAZguq%2bj5oGNMAv2AjrG31BvR1NC5QDl23OMQrOG6stdsz6dqafZxPErTdwiEDkCUWHj6TF%2f04HzwoolSI4T1FY2loLpn00WBbMgxKhU13fnREb3MyYa4WVZbav6dbYARgz6ibJGKUn1Kb5qodbQ6M7NcZXJ9odIo80RXdE%2fBqQaUgIAG4jtgYWu8oI4TG6e16GKP0Gy1PM5XsMtDL47q6mbfNPfN7g6ttOdrWp1Pb6iLebJcf3AcAPjgjwZxTEB%2fIt1iSd%2bspuzU9FD4SY%2bAaXlwGoHwWGdIKn1kBLZF5W0nZW%2f1z7o%2fO7e6%2f8i2lDYe2Ys7meUthx9ZpNyF4CyZOwnv%2fknNJtCEtzhluFtSyxN78eSPMuGqFgp7zeAzXhjEY9zbDRrBdIfVYGVsFdqfd7e3IrRR9znFjPoqHa99MDIyvHU4yb3gRR3BnR9zo2QEV6dwV%2fvuM2ruuk51O%2fuHiI%3d&_eventId=submit&submit=%E7%99%BB%E5%BD%95"
        body_for_activity ="username=jinjin.huang%40mi-me.com&password=123456&lt=LT-4081-PPLNtCrDec9fE6i3JhDCxCNEAo14S2-cas01.example.org&execution=0d6d0202-7ca8-4b60-bc2c-b6985c47fc10_AAAAIgAAABCK7TV2v7aEHHs0ng1TsD6YAAAABmFlczEyOD5m%2BgxNOahJ1aGVL26inJmZjNVOy6j2oebpwyzFy9sKCSzBXGqpGiH2t1dzdiwX1tagOxyr9PbsoCoXSZ4%2BsoGrIj5EsSnXGvjkUYhOuoNxcAVJrV06URGenmRr1ZnoJ5Uyzg%2FgpeRtSVkpaluIjWIXo7hqC21zwpLH0iSixX7k3OhD4bBBsNjwlrObc0y%2FkZQXv0ciV5NCGLe6NXNrZax7LuYE6Yx3pn%2BfFhEg%2B%2BSL2VFql5tKPm%2B5yIYMcKFWx%2Fjb0r5bMO41d6KGr2DbAhOMQxZ41kHfC6i%2FVuam7BEYwZJ70cSoO86FEs3iRpsRycgiERKldhXce1CKiEPgE6%2BSK0%2FAyTxPDfHU%2FGxA63nIb3R7yGdcZGo3rlIH5rXFIrUBtANalKOdKtrKrjYCFrir9QAdpjq%2FvcG9SN5FNOv7vrXavOSA6qTrNT31GhW4Skj1av498OXASUbcvwXXKNQFqk3bfVAcSKguEUD86BpZiGJfKAPDu5CMnNB4ml51k5rW6gH7wAsn2VnenQNpXAFob2lkNYKOdk5voxBzXL9NvxRWcvOcb%2B8d2OreAZlpn84QNssA5s79CWzrMzdeGFbFXRgTdSemBNOnX0Kb6gA90jTIewiaQoyNqmHlSqx3DMDYqCRERTINwT8VTMzIoTi1tnVqHcPb48NHknpMaNo%2FFdTdAI0tPdqOYBit1wDmxK1hXE%2BmVAp%2BNPEc26PeBlQX0177NhgB5jMFChgOd%2BNQu%2BLSU%2Fz0Z2xm8Aq7fVCJKosaCgqOXBvPUq3UMNdIdxmjMsgk6cvSuNHc8tM03hiO0JMRpWVxIrrcgB0gt43I4TOFZPWSOuqaZ78J5qyyeEYrUute2SlfgSk2AktwVGotRNL3ZXyB%2FoZspMOXFLjecnbncp0PHajWvQDFlojv30%2Fky5p%2FcYuQY0mwE%2FeZeTowkYckVDWEn7eOSCJEwCWZ%2FmPr99ASGiaR0BRU9Q%2F2v34Y7E6zRWsFud1uTd1ALKamubsI8ERozlsjmx1RPHr2euZrfZdvmFRNqeK2DZXgHuelevHpCke0OFAkZ3hEABCsFO1WFX%2F9uu6quUWRTRXimcGAs%2BZks3GtB%2BBf9lzSwUSOE%2BRuhBEeSnHNn%2B1OuarowHiS7XKrf1b50ZExItq8BZoP8x6yXNCy1YFxn4gVq7Mh8sE7PSR3L4Ks2Q5pduaB42GBwiEZlCci95sfNMBigAs67Gc7PZkSO1OHaVXf%2FbsKorUYhyx4gf8NGyFTw9CgUey7%2FIbuJXAuohwwu%2FNJRY3PTgedBX04HNxvqMDygSrDhLTxmUWkwt5S7UEmlcvQFxwUIf88n9tV%2F%2BAryGefQfh4vIWSnWrra%2F1Y3OvtVYDhvAIZE6e5Oyg05apvwdmw%2F7p91sq10DPAR98b1K%2BA9axPLjoK1EJ%2B%2BLCiNd8RCNXTvY%2FPlqK5lMOlhWzQDXsehbnF6DRxxDxdWG0d0g9ZgreLHWYeF6OTVpQflcPjzsSfTDeyLFBw5FYkBhuUeIHutbhua4ouKa07t9rDxAVrMl7X1ra7NgA8rjPEX1Sc26y0vAOKywVl2Uef9h9nY58YCtCSQLYFBIbq252kqFTvwdBNJ2uRDYD5RAY7bPFDHlMYvzzoh0mk3CSalu5V8RqffjeaiwDNxAB%2F5xwZcIncNUUUKU0QnGtkLGua9FCjDkPBOzAz4zvBKRlwscp0kBWaHi0W0XTqh7RHMpzHTSLKnwCS2Xb1RkyEYYrPUzhbHzdZgSNTuFgjwPww9a7n33Usw9%2FNEP%2FQRveVMLAwwHj25PNF%2F5o54ZJ5s%2Bm%2FfZiLGndgkXnqKkDdyGaT9B%2FUuij36CXM2z7um3u3AXSZ9mSn33XMN%2B90osYl85d63Gk8XW2UYjak40Q63XmdCcMJbZ74PZG2gr2bKfS4xSMCfuwezPboR7KR2XUdtpbz0bCPQrGxZo%2BNRsnKNJnoTTz1quPh8%2FjtV69cGN3pD%2B8dZL9M%2Fxw0cGIeXQ4kqRC2VwdmH5sIRghndBypo6w374%2BlPQAtjWlpihccOtZbMBx5KcTV0y0v4G3bkn3Yh6WkEwmtzOFSp3XZ1MxDxGLSLmimzdHEZNa0HX445cu8YW%2BeVJ5%2FGqSrm0wRaS6olC%2BLyAblAIbgEUyMWpjtkp68MhN%2FhMxyS836REhdrAv5paCBPuzWFe80F4566Hv3ERI%2FvmstJ8WXsiRTUKGTUkNCe%2BgjVlQpLzVhkDZ0Uv5Tuq6FivaHMp26XBJwQzNiJWZeOC50xHFYUcd1OtUx0XC6Nj6bUYwTZx1XBeuwZG4PjBQ0j6DKu9R%2BFxJbyj7Nqd2noaauFemzL802qHPMM%2FNPEckPtMRf3rja%2B1cevbRPbAeZFNfFj%2BXJJiuG%2FzgWsQsJ%2BDMxYpkstifIz%2FJ3hutaabugxAb1OuYOAcqSMh%2FRrQ8jrI4ENYxQ0lyML8jum9PHyAw%2FbQc1VLy9OQtG5K2EKwFbZQRA&_eventId=submit&submit=%E7%99%BB%E5%BD%95"
        
        if 'couponManagement' in url:
            body = body_for_coupon
        elif 'activityManagement' in url:
            body = body_for_activity

        else:
            body = body_for_cta
        try:
            respose = self.http_post(url,heard_info,body)
            # 对返回状态非302状态直接抛异常
            if respose.status_code != 302:
                raise Exception(respose)
            redirect_url = respose.headers['Location'] # 获取重定向的url

            respose = self.http_get(redirect_url,heard_info) # 请求重定向url
            # 对返回状态非200状态直接抛异常
            if respose.status_code != 200:
                raise Exception(respose)
            jSessionId = respose.headers['Set-Cookie'] # 获取JSESSIONID


        except Exception as err:
            print '\n'.join([str(err), traceback.format_exc()])
            logger.info("SSO单点登录失败")
            raise err

        return jSessionId

if __name__== '__main__':
    pass