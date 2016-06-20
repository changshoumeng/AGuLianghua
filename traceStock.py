# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng

'''
http://quote.hexun.com/default.html
http://quote.tool.hexun.com/hqzx/getstock.aspx?stocklist=000001_1|399001_2&time=231850

http://webstock.quote.hermes.hexun.com/a/quotelist?code=sse000001&column=DateTime
,LastClose,Open,High,Low,Price,Volume,Amount,LastSettle,SettlePrice,OpenPosition,
ClosePosition,BuyPrice,BuyVolume,SellPrice,SellVolume,PriceWeight,EntrustRatio,
UpDown,EntrustDiff,UpDownRate,OutVolume,InVolume,AvePrice,VolumeRatio,
PE,ExchangeRatio,LastVolume,VibrationRatio,LastVolume,VibrationRatio,DateTime,OpenTime,CloseTime
'''

import urllib,urllib2,cookielib,socket,time,random
from urllib2 import URLError, HTTPError
import traceback 
import sys
import json
from common import *
from stockdesc import *
import alarmReport
socket.setdefaulttimeout(9)



class GetStockRequst:
    def __init__(self,szCode):
        self.szCode=szCode
        self.url=""
        self.json_str=""
        pass
    def get_jsonstr(self,rsp):
        s1=""
        pos1=rsp.find("[")    
        if pos1 < 0:
            return s1
        pos2=rsp.rfind("]")
        if pos2 < pos1:
            return s1
        s1=rsp[pos1:pos2+1]
        return s1
        
        
    def parse_jsonstr(self,json_str):
        global todayMyStockDir
        try:
            json_data = json.loads(json_str)
            if len(json_data) != 1:
                print "parse_jsonstr len-error:",json_str
                return
            
            item=json_data[0]
            code=item['Code']
            
            fileName=r'{0}/{1}.txt'.format(todayMyStockDir,code)
            with open(fileName,'a') as f:
                item['date']=getNowHourMinute()     
                self.json_str=json.dumps(item)
                f.write(self.json_str)
                f.write('\n')
        except:
            print "parse_json error:",json_str    
    def doGetBySocketClient(self):   
        res="columns=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26&codes={0}".format(self.szCode) 
        host = '61.155.222.183'  
        port = 80  
        bufsize = 4096  
        addr = (host,port)  
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        result=""
        try:
             client.connect(addr) 
             data='''GET /QuoteData/newquote.ashx?{0} HTTP/1.1\r\nHost: data.mymoney.hexun.com\r\n
            Connection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36\r\n
            Accept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n\r\n'''.format(res) 
             client.send(data)          
             while True:
                 d=client.recv(bufsize)
                 if d==None or len(d)==0:
                     break
                 result += d
        except:
             (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
             print "Connect server failed: ", ErrorValue
             result=""
             
        client.close()        
        return  result
    def  doGet(self):
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
       # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        #opener = urllib2.build_opener(httpHandler, httpsHandler)
        #urllib2.install_opener(opener)
        request = urllib2.Request(self.url)
        #request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        #request.add_header('Content-Type', 'application/x-www-form-urlencoded')
       # request.add_header('Host','chelun.eclicks.cn')   
        try:
            response = urllib2.urlopen(request,timeout=10)
            page = response.read()     
            #print len(page)
            return page
            #print response.info(),re
        except URLError,e:   
            if hasattr(e, 'code'):    
                print('The server couldn\'t fulfill the request. errorcode:{0}'.format(e.code ))                  
            elif hasattr(e, 'reason'): 
                print('We failed to reach a server. reason:{0}'.format(e.reason ))                           
        except:   
            print traceback.format_exc()
           
            #print page.decode("utf-8")               
        return ""    
    def run(self):
        rsp=self.doGetBySocketClient()
        if len(rsp)==0:
            print "doGetBySocketClient failed"
            return
        json_str=self.get_jsonstr(rsp)            
        if len(json_str)==0:
            print "get_jsonstr failed"
            return
        self.parse_jsonstr(json_str)           
            
        
class GetZhiShuRequst:        
    def __init__(self):     
        self.url=""
        pass     
    def get_jsonstr(self,rsp):
        s1=""
        pos1=rsp.find("[")    
        if pos1 < 0:
            return s1
        pos2=rsp.rfind("]")
        if pos2 < pos1:
            return s1
        s1=rsp[pos1:pos2+1]
        return s1       
    def parse_jsonstr(self,json_str):
        global todayMyStockDir
        try:
            json_data=eval(json_str)            
            for item in json_data:
                print item                             
               
        except:
            print "parse_json error:",json_str            
    def  doGet(self):
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
       # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        #opener = urllib2.build_opener(httpHandler, httpsHandler)
        #urllib2.install_opener(opener)
        tm=time.time()
        tm=int(tm)%12345
        self.url='http://quote.tool.hexun.com/hqzx/getstock.aspx?stocklist=000001_1|399001_2&time={0}'.format(tm)
        request = urllib2.Request(self.url)
        #request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        #request.add_header('Content-Type', 'application/x-www-form-urlencoded')
       # request.add_header('Host','chelun.eclicks.cn')   
        try:
            response = urllib2.urlopen(request,timeout=10)
            page = response.read()     
            #print len(page)
            return page
            #print response.info(),re
        except URLError,e:   
            if hasattr(e, 'code'):    
                print('The server couldn\'t fulfill the request. errorcode:{0}'.format(e.code ))                  
            elif hasattr(e, 'reason'): 
                print('We failed to reach a server. reason:{0}'.format(e.reason ))                           
        except:   
            print traceback.format_exc()
           
            #print page.decode("utf-8")               
        return ""   
    def run(self):
        rsp=self.doGet()        
        if len(rsp)==0:
            print "doGetBySocketClient failed"
            return
        json_str=self.get_jsonstr(rsp)  
         
        if len(json_str)==0:
            print "get_jsonstr failed"
            return
        self.parse_jsonstr(json_str)           
  



def minute_get_stock_data(pinyin,Code,history_list,upRateLimit,downRateLimit,upPriceLimit,downPriceLimit):    
    req=GetStockRequst(Code)
    req.run()    
    #print req.json_str
    stockObj=Stock(pinyin,req.json_str) 
    
    stockObj.printInfo()
    if None != history_list:
        history_list.append(stockObj)
    if upRateLimit != 0 and stockObj.Rate >= upRateLimit:
        title="{0}".format(Code)
        text="Rate:{0} >= upRateLimit:{1}".format(stockObj.Rate,upRateLimit)
        alarmReport.reportAlarm(title,text)
        pass
    if downRateLimit != 0 and stockObj.Rate <= downRateLimit:
        title="{0}".format(Code)
        text="Rate:{0}  <= downRateLimit:{1}".format(stockObj.Rate,downRateLimit)
        alarmReport.reportAlarm(title,text)
        pass        
    if upPriceLimit != 0 and stockObj.Price >= upPriceLimit:
        title="{0}".format(Code)
        text="Price:{0} >= upPriceLimit:{1}".format(stockObj.Price,upPriceLimit)
        alarmReport.reportAlarm(title,text)
        pass
    if downPriceLimit != 0 and stockObj.Price <= downPriceLimit:
        title="{0}".format(Code)
        text="Price:{0} <= downPriceLimit:{1}".format(stockObj.Price,downPriceLimit)
        alarmReport.reportAlarm(title,text)
        pass    
    return stockObj    
#    if downPriceLimit != 0 and stockObj.Rate >= downPriceLimit:
#        title="{0}".format(Code)
#        text="Rate:{0} >= upRateLimit:{1}".format(stockObj.Rate,upRateLimit)
#        alarmReport.reportAlarm(title,text)
#        pass
#    if upRateLimit != 0 and stockObj.Rate >= upRateLimit:
#        title="{0}".format(Code)
#        text="Rate:{0} >= upRateLimit:{1}".format(stockObj.Rate,upRateLimit)
#        alarmReport.reportAlarm(title,text)
#        pass   

def minute_get_zhishu_data(pinyin,Code,policy):
    req=GetStockRequst(Code)
    req.run()       
    stockObj=Stock(pinyin,req.json_str,policy)        
    stockObj.doIt() 
    return stockObj    




def main():     
    mkdir(todayMyStockDir)
    #req=GetStockRequst("sse000001")
    req=GetStockRequst("sse000001")
    req.run()    
    stockObj=Stock(req.json_str)
    print stockObj.Price,stockObj.Rate,stockObj.Amount

def test():
    req=GetZhiShuRequst()
    req.run()   
    pass


if __name__=="__main__":  
    print __file__
    mkdir(todayMyStockDir)
    jingugufen002488=[]
    upRateLimit=1
    downRateLimit=-2
    upPriceLimit=0
    downPriceLimit=0    
    #minute_get_stock_data("szse002488",jingugufen002488,upRateLimit,downRateLimit,upPriceLimit,downPriceLimit)
    #minute_get_stock_data("szse002208",jingugufen002488,upRateLimit,downRateLimit,upPriceLimit,downPriceLimit)
       

