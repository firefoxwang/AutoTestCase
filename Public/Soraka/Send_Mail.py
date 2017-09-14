# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from email.header import Header

'''
Created on 2016-12-6
 
@author: Rudolf Han
'''

def send_email(send_info,email_info,project_mails,email_content,send_annex=None):
   # sender =send_mail #发送人
   # receivers = receivers_mail  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #创建一个带附件的实例
    message=MIMEMultipart()
    message['From'] = Header(email_info["From"], 'utf-8') #发件人显示
    message['To'] =  Header(email_info["To"], 'utf-8')  #收件人
#    subject = Subject  
    message['Subject'] = Header(email_info["Subject"], 'utf-8') #邮件标题

    #邮件正文内容
    message.attach(MIMEText(email_content, 'plain', 'utf-8'))
    # 构造附件1，传送当前目录下的 test.txt 文件
    if  send_annex != None:
        message.attach(MIMEText(email_content, 'html','utf-8'))
        for i in send_annex ["send_name"]:
            att = MIMEText(open(send_annex["send_path"]+i, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att["Content-Disposition"] = 'attachment; filename="'+i+'"'
            message.attach(att)
#        # 构造附件2，传送当前目录下的 runoob.txt 文件
#        att2 = MIMEText(open(send_annex["send_path"]+send_annex["send_log"], 'rb').read(), 'base64', 'utf-8')
#        att2["Content-Type"] = 'application/octet-stream'
#        att2["Content-Disposition"] = 'attachment; filename="'+send_log+'"'
#        message.attach(att2)

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(send_info["send_host"],send_info["send_port"])    # 25 为 SMTP 端口号
        smtpObj.login(send_info["send_mail"],send_info["send_pwd"])
        smtpObj.sendmail(send_info["send_mail"], project_mails, message.as_string())
        print "send mail sucess"
    except smtplib.SMTPException:
        print "Error: send mail faile"
