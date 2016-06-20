# -*- coding: utf-8 -*-
#Give wisdom to the machine
import json
from common import *
import alarmReport

class Policy(object):
    def __init__(self):
        self.upRateLimit = 0.0
        self.downRateLimit = 0.0
        self.upPriceLimit = 0.0
        self.downPriceLimit = 0.0
        self.zuotAmount= 0.0
        self.zuotRate=0.0
        self.upTurnover=0.0
        self.downTurnover=0.0
        self.amplitude=0.0

class Stock(object):
    def __init__(self,pinyin='',json_str='',policy=None):
        self.json_str = json_str
        self.FS=0.0#总股本
        self.TMV=0.0#总市值
        self.EPS=0.0#每股收益
        self.Low=0.0#最低价
        self.CMV=00#流通市值
        self.Volume=0.0#成交量
        self.NAPS=0.0#每股净资产
        self.Price=0.0#当前股价
        self.POR=0.0#主要收入
        self.ROE=0.0#净资产收益率
        self.PB=0.0#市净率
        self.PE=0.0#市盈率
        self.Change=0.0#涨跌
        self.PreClose=7.2#昨收盘
        self.Amount=0.0#成交额度
        self.Turnover=0.0#换手率
        self.Code=0#证券编码
        self.High=0.0#最高
        self.Rate=0.0#涨跌百分比
        self.Open=0.0#今开
        self.Amplitude=0.0#振幅
        self.Market=0.0       
        self.date=0
        self.pinyin=pinyin
        self.policy=policy
        self.__readData__()
    def __readData__(self):
        try:
            json_object=json.loads(self.json_str)
            self.FS=json_object["FS"]
            self.TMV=json_object["TMV"]
            self.EPS=json_object["EPS"]
            self.Low=json_object["Low"]
            self.CMV=json_object["CMV"]
            self.Volume=json_object["Volume"]
            self.NAPS=json_object["NAPS"]
            self.Price=json_object["Price"]
            self.POR=json_object["POR"]
            self.ROE=json_object["ROE"]
            self.PB=json_object["PB"]
            self.PE=json_object["PE"]
            self.Change=json_object["Change"]
            self.PreClose=json_object["PreClose"]
            self.Amount=json_object["Amount"]
            self.Turnover=json_object["Turnover"]
            self.Code=json_object["Code"]
            self.High=json_object["High"]
            self.Rate=json_object["Rate"]
            self.Open=json_object["Open"]
            self.Market=json_object["Market"]
            self.date=json_object["date"]
            self.Amplitude = 0.0
            n1=self.High-self.Low
            if self.PreClose != 0:
                self.Amplitude=n1/self.PreClose
        except:
            print "except,loads Jsonstr error:",self.json_str            
        
        pass    
    
    def doIt(self):         
        title="{0}".format(self.Code)        
        if  self.policy.upRateLimit != 0 and self.Rate >=  self.policy.upRateLimit:            
            text="Rate:{0} >= upRateLimit:{1}".format(self.Rate,self.policy.upRateLimit)
            alarmReport.reportAlarm(title,text)
            self.policy.upRateLimit += 0.2           
            return
            pass
        if self.policy.downRateLimit != 0 and self.Rate <= self.policy.downRateLimit:            
            text="Rate:{0}  <= downRateLimit:{1}".format(self.Rate,self.policy.downRateLimit)
            alarmReport.reportAlarm(title,text)           
            self.policy.downRateLimit -= 0.2
            return
            pass        
        if self.policy.upPriceLimit != 0 and self.Price >= self.policy.upPriceLimit:             
            text="Price:{0} >= upPriceLimit:{1}".format(self.Price,self.policy.upPriceLimit)
            alarmReport.reportAlarm(title,text)
            self.policy.upPriceLimit += 10           
            return
            pass
        if self.policy.downPriceLimit != 0 and self.Price <= self.policy.downPriceLimit:            
            text="Price:{0} <= downPriceLimit:{1}".format(self.Price,self.policy.downPriceLimit)
            alarmReport.reportAlarm(title,text)           
            self.policy.downPriceLimit -= 10
            return
            pass
        if self.policy.upTurnover != 0 and self.Turnover >= self.policy.upTurnover:            
            text="Turnover:{0} >= upTurnover:{1}".format(self.Turnover,self.policy.upTurnover)
            alarmReport.reportAlarm(title,text)           
            self.policy.upTurnover += 0.2
            return
            pass    
                    
                    
    
    def printInfo(self):
        pass
        data="[{0}_{1}]price:{2}|{3} HighLow:{4}|{5} Turnover:{6}".format(self.pinyin,self.Code,self.Price,self.Rate,self.High,self.Low,self.Turnover)
        print data
    def getShanghaiInfo(self):
        #1241.51
        zt_amount=self.policy.zuotAmount
        #zt_amount=1178*(10**8)
        zt_percent=(self.Amount*100)/ zt_amount
        should_amount=getCurrentChangeMinite(self.date)/240.0*zt_amount
        actual_amount=(self.Amount*100)
        dif_amount=actual_amount-should_amount
        dif_percent=dif_amount/should_amount        
        data="[{0}_{1}]price:{2}|{3} HighLow:{4}|{5} Cjl:{6:.4f}|{7:.3f}".format(self.pinyin,self.Code,self.Price,self.Rate,self.High,self.Low,zt_percent,dif_percent)        
        return data
    
    def getCyInfo(self):
        #1241.51        
        data="[{0}_{1}]price:{2}|{3} HighLow:{4}|{5} ".format(self.pinyin,self.Code,self.Price,self.Rate,self.High,self.Low)        
        return data    






if __name__=="__main__":  
    pass
    #print __file__
    #p=Policy()
    #p.upRateLimit=-2
    #json_str='''{"FS": 14308.68, "TMV": 0.0, "EPS": 0.0, "Low": 2789.47, "CMV": 0.0, "Volume": 73324820.48, "NAPS": 0.12, "Price": 2794.29, "POR": 275319992.32, "ROE": 0.03, "PB": 0.0, "PE": 0.0, "NP": 60860001.28, "Change": -49.39, "PreClose": 2843.68, "Amount": 788331806.72, "date": "12:17:27", "Turnover": 0.0, "Code": "000001", "High": 2828.26, "Rate": -1.74, "Open": 2828.18, "Market": 2}'''   
    #s=Stock("",json_str,p)
    #s.printInfo()    
    #print s.FS 
    #s.doIt()
    #s.doIt()
    #s.doIt()
    
    pass


'''
 编码       名称     marketType   当前指数     开盘     最低    最高     涨跌     涨跌百分比
['000001','上证指数','1',         2794.29, 2828.18,2789.47,2828.26,-49.39,-1.74,      788]


sse000001 上证
szse002488 金固股份
'''        