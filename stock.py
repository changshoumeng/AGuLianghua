# -*- coding: utf-8 -*-
#Give wisdom to the machine
'''
http://quote.hexun.com/default.html
'''

import urllib,urllib2,cookielib,socket,time,random
from filelock import FileLock
import threading
from matplotlib.dates import datetime
import os
from common import *

timer_seconds=10



    


def get_request(url):  
  #可以设置超时  
  socket.setdefaulttimeout(5)  
  #可以加入参数  [无参数，使用get，以下这种方式，使用post]  
  #params = {"wd":"a","b":"2"}  
  #可以加入请求头信息，以便识别  
  i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER",  
             "Accept": "*/*",
             "Accept-Encoding":"gzip, deflate, sdch",
             "Connection":"keep-alive",
            "Host":"quote.tool.hexun.com",  
            "Accept-Language":"zh-CN,zh;q=0.8"
             }  
  #use post,have some params post to server,if not support ,will throw exception  
  #req = urllib2.Request(url, data=urllib.urlencode(params), headers=i_headers)  
  req = urllib2.Request(url, headers=i_headers)  
  
  #创建request后，还可以进行其他添加,若是key重复，后者生效  
  #request.add_header('Accept','application/json')  
  #可以指定提交方式  
  #request.get_method = lambda: 'PUT'  
  try:  
    page = urllib2.urlopen(req)  
    return  page.read()
    #print len(page.read())  
    #like get  
    #url_params = urllib.urlencode({"a":"1", "b":"2"})  
    #final_url = url + "?" + url_params  
    #print final_url  
    #data = urllib2.urlopen(final_url).read()  
    #print "Method:get ", len(data)  
  except urllib2.HTTPError, e:  
    print "Error Code:", e.code  
  except urllib2.URLError, e:  
    print "Error Reason:", e.reason
  return "" 

'''
代码	名称	最新价	涨跌幅	昨收	今开	最高	最低	成交量	成交额	换手	振幅	量比
0       1     2     3      4     5      6      7      8      9    10     11     12
'''
def splitLine(line):
    global todayShanghaiStockDir
    a=line.split(",")
    stockCode=a[0]  
    #aaa=int(stockCode)
    stockCode=stockCode.replace('\'','')  
    fileName=r'{0}/{1}'.format(todayShanghaiStockDir,stockCode  ) 
    with open(fileName,'a')  as f:
        line2='{0},{1}\n'.format(getNowHourMinute(),line)
        f.write(line2)        
    return a

  

def parseResponse(response,stockList):
    begin=0
    pos=response.find("[",begin)
    begin=pos+1
    k=0    
    while True:
        pos1=response.find("[",begin)
        if pos1 <0:
            break
        pos1 +=1
        #print pos1
        begin=pos1+1
        pos2=response.find("]",begin)
        if pos2 <0:
            break
        #print pos2
        line= response[pos1:pos2]
        a=splitLine(line)
        stockList.append(a)
        begin=pos2+1
        k += 1
        if k > 5:
            pass
            #break
    #print len(stockList)
    pass
    
getIndex=0    
def getStockList():
    global getIndex
    getIndex += 1
   # for i in xrange(1,23,1):  
    stockList=[]  
    for i in xrange(1,7,1):      
        tm=getIndex+100610
        url="http://quote.tool.hexun.com/hqzx/quote.aspx?type=2&market=1&sorttype=3&updown=up&page={0}&count=200&time={1}".format(i,tm)
        response=get_request(url)
        parseResponse(response,stockList)    
        
    return  stockList
    

    
'''
代码	名称	最新价	涨跌幅	昨收	今开	最高	最低	成交量	成交额	换手	振幅	量比
0       1     2     3      4     5      6      7      8      9    10     11     12
'''
def fenxiStockList1(stockList): 
    item=FenxiItem1()
    
    topline=float(8.0)
    zeroline=float(0.0)
    bottomline=float(-8.0)   

    '''
    '600000','浦发银行',17.50,-0.06,17.51,17.38,17.52,17.38,4603.35,8035230,0.00,0.80,0.99
    '''
    for stock in stockList:      
        item.total += 1
        rise_rate = float( stock[3])

        item.zuixinjia += float( stock[2] )     
        item.zhangdiefu += float( stock[3] )  
        item.zuoshou += float( stock[4] )  
        item.jinkai += float( stock[5] )  
        item.zuigao += float( stock[6] )  
        item.zuidi += float( stock[7] )  
        item.chengjiaoliang += float( stock[8] )  
        item.chengjiaoqian += float( stock[9] )  
        item.huanshou += float( stock[10] ) 
        item.zhenfu += float( stock[11] )
        item.liangbi += float( stock[12] )
        
        if rise_rate >= topline:
            item.rise_top += 1
            item.rise     += 1
        elif  zeroline < rise_rate < topline:
            item.rise     += 1
        elif  bottomline<rise_rate <zeroline:
            item.fall += 1
        elif   rise_rate ==  zeroline:
            item.keep_zero += 1
        elif rise_rate <= bottomline:
            item.fall += 1
            item.fall_bottom += 1
        if   -1.0 <= rise_rate <= 1.0:
            item.keep_one += 1
            if 0<=rise_rate <= 1.0:
                item.keep_one1 += 1
    return item          




 

 
def func():
    global timer_seconds   
    runOnce() 
    timer = threading.Timer(timer_seconds, func)
    timer.start() 
            
def runOnce():
    if False == isChangeTime():        
        return    
    try:
        update_globalvar()
        stockList=getStockList()  
        item1= fenxiStockList1(stockList)
        item1.dump()  
    except:
        pass        

def main():
    global timer_seconds
    runOnce()
    timer = threading.Timer(timer_seconds, func)
    timer.start() 
    
    
if __name__ == "__main__":  
    print "main enter"   
    print "today dir is :",todayDir
    mkdir(  todayDir      )
    mkdir( todayShanghaiStockDir )
    mkdir( todayShenzhenStockDir )  
    main()
#    while True:
#        c=raw_input("please input e:")
#        if c=='e':
#            print "finished"
#            break        
    print "main leave"


