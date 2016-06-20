# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng
#    code="sse603528"
#code="szse603528"
from stockdesc import *
from common import *
import threading
from traceStock import *


p1=Policy()
p1.upRateLimit=0
p1.downRateLimit=-5
p1.upPriceLimit=22
p1.downPriceLimit=20.3
p1.upTurnover=10

def onceWork():
    if False==isChangeTime():
        pass
        #return    
 
    pinyin="me"
    #code="sse603528"
    code="szse002488"
    stockObj=minute_get_zhishu_data(pinyin,code,p1)       
    stockObj.printInfo()

def func():
    onceWork()
    timer = threading.Timer(5, func)
    timer.start()   

def startTimer():
    timer = threading.Timer(1, func)
    timer.start()      

if __name__=="__main__":  
    print __file__
    mkdir(todayMyStockDir)
    startTimer()
    onceWork()
       