# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng
#7 15 146 210
#
import alarmReport
from stockdesc import *
from common import *
import threading
from traceStock import *
from xlsxprocess import  *


##############################################################
p1=Policy()
p1.upRateLimit=0.5
p1.downRateLimit=-0.5
p1.upPriceLimit=2850
p1.downPriceLimit=2800
p1.zuotAmount=1632789790.72

def shanghaiWork():     
    pinyin="sh"
    code="000001"
    zode="sse000001"
    if p1.zuotAmount == 0:
        data=getLastAmout(code)
        print "getLastAmount:",data
        if data :
            (open, close, high, low, amount, turnover, amplitude, rate)=data
            p1.zuotAmount=float(amount)*100
            p1.zuotRate=float(rate)
            p1.upTurnover=turnover
            p1.amplitude=amplitude
    stock=minute_get_zhishu_data(pinyin,zode,p1)
              
    updateXlsx(code,stock.Open,stock.Price,stock.High,stock.Low,stock.Amount,stock.Turnover,stock.Amplitude,stock.Rate,stock.date)
    return stock
    

##############################################################
p2=Policy()
p2.upRateLimit=0.5
p2.downRateLimit=-0.5
p2.upPriceLimit=2100
p2.downPriceLimit=2040
def chuangyeWork():    
    pinyin="cy"
    code="szse399006" 
    stock=minute_get_zhishu_data(pinyin,code,p2)    
    return stock
    
    
    

##############################################################
def onceWork():
    if False==isChangeTime():
        return
    shanghai=shanghaiWork()
    chuangye=chuangyeWork()
    info1=shanghai.getShanghaiInfo()
    info2=chuangye.getCyInfo()
    print info1,info2


##############################################################
def func():
    onceWork()
    timer = threading.Timer(5, func)
    timer.start()   
    


##############################################################
def startTimer():
    timer = threading.Timer(1, func)
    timer.start()      


##############################################################
if __name__=="__main__":  
    print __file__
    mkdir(todayMyStockDir)
    #onceWork()
    startTimer()
       