# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng

from sendmail import * 
import win32api,win32con
import time
import socket
import sys
import struct

'''邮件报警'''
def reportMail(title,text):
    server=dict()
    server['name']='smtp.163.com'
    server['user']='zhangtaolmq'
    server['passwd']='4495@7'
    fro='zhangtaolmq@163.com'
    to=['3374132290@qq.com']
    subject=title
    #text='text 1'
    files=[]
    send_mail(server, fro, to, subject, text, files)
    print "reportMail:",title
    pass


'''弹出框警告：这个警告会阻塞，想办法弄成异步'''    
def reportDialog(title,text):    
    win32api.MessageBox(0, text,title,win32con.MB_OK)
 

def packStringData(stringdata):     
    length=len(stringdata)
    formatStr="!I%ds"%(length)       
    data=struct.pack(formatStr,length,stringdata)
    return data   
    
def reportDialog2(title,text):      
    host = '127.0.0.1'  
    port = 1997  
    #bufsize = 4096  
    addr = (host,port)  
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    try:
         client.connect(addr) 
         data=packStringData(text.encode("gbk"))   
         print "send:",    client.send(data) 
         
    except:
         (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
         print "Connect server failed: ", ErrorValue
         
    client.close()            
    
    
'''报警接口'''
def reportAlarm(title,text):    
    nowTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    text= u"-"+text
    text=u"[{0}][{1}]say:{2}".format(nowTime,title,text)
    print text
    #reportMail(title,text)
    reportDialog2(title,text)
    
    
    

if __name__ == '__main__':
    reportDialog2("TEST",u"你好{0}".format(u"0021455你好得到"))        
    
