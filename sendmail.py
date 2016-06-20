# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# python 2.3.*: email.Utils email.Encoders
from email.utils import COMMASPACE,formatdate
from email import encoders
import smtplib
import os

#server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', '
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))
    
    for file in files:
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        part.set_payload( open(file, 'rb').read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)
    
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()

#def main():
#    server=dict()
#    server['name']='smtp.163.com'
#    server['user']='zhangtaolmq'
#    server['passwd']='4495@7'
#    fro='zhangtaolmq@163.com'
#    to=['406878851@qq.com']
#    subject='title'
#    text='text 1'
#    files=[]
#    send_mail(server, fro, to, subject, text, files)
#    pass

if __name__ == '__main__':
    pass
    import win32api,win32con
    import time
    time.sleep(3)
    win32api.MessageBox(0, u"TEST", u"TEST",win32con.MB_OK)
    #main()