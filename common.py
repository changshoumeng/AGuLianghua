# -*- coding: utf-8 -*-

import time,os
from filelock import FileLock
from backwardreader import * 
from matplotlib.dates import datetime

def getNowMinuteIntVal(s):
    try:
        tm = time.strptime(s,"%H:%M:%S")
        return tm.tm_hour*60+tm.tm_min
    except:
        return 0

    open("").readl

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    
def getNowHourMinute():
    return time.strftime("%H:%M:%S",time.localtime(time.time()))    
    
def getCurrentChangeMinite(nowTimeStr):    
    begin_time1=getNowMinuteIntVal("09:30:00")
    end_time1=getNowMinuteIntVal("11:30:00")
    begin_time2=getNowMinuteIntVal("13:00:00")
    end_time2=getNowMinuteIntVal("15:00:00")
    now_time=getNowMinuteIntVal(nowTimeStr)
    if begin_time1<=now_time<=end_time1:
        return now_time-begin_time1
    if begin_time2<=now_time<=end_time2:
        return now_time-begin_time2+120
    return 0        
    
'''获取文件后缀名'''
def get_file_extension(file):  
    return os.path.splitext(file)[1]  

'''創建文件目录，并返回该目录'''
def mkdir(path):
    # 去除左右两边的空格
    path=path.strip()
    # 去除尾部 \符号
    path=path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        
    return path

def getNowDay():
    return time.strftime("%m_%d",time.localtime(time.time()))
   
   
''' 全局变量'''   
todayDir=getNowDay() 
todayShanghaiStockDir=r'{0}/ss'.format(todayDir)
todayShenzhenStockDir=r'{0}/sz'.format(todayDir)
todayShanghaiFile=r'{0}/ss_file.txt'.format(todayDir)
todayShenzhenFile=r'{0}/sz_file.txt'.format(todayDir)
todaysszdFile=r'{0}/ss_zd.txt'.format(todayDir)
todayMyStockDir=r'{0}/my_stock'.format(todayDir)


def update_globalvar():
    global todayDir
    global todayShanghaiStockDir
    global todayShenzhenStockDir
    global todayShanghaiFile
    global todayShenzhenFile
    global todaysszdFile
    todayDir=getNowDay() 
    todayShanghaiStockDir=r'{0}/ss'.format(todayDir)
    todayShenzhenStockDir=r'{0}/sz'.format(todayDir)
    todayShanghaiFile=r'{0}/ss_file.txt'.format(todayDir)
    todayShenzhenFile=r'{0}/sz_file.txt'.format(todayDir)
    todaysszdFile=r'{0}/ss_zd.txt'.format(todayDir)


def readLastLineFromFile():
    global todayShanghaiFile
    line=""
    try:
        with open(todayShanghaiFile,'r') as f:       
                br=BackwardsReader(f)
                line=br.readline()
                while len(line) < 5:
                    line=br.readline()
    except Exception as e:
        print "readLastLineFromFile:",e
    except:
        print "readLastLineFromFile: unknow Exception"  
    return line


def readLineListFromFile():
    global todayShanghaiFile
    lineList=[]
    try:
        with open(todayShanghaiFile,'r') as f:       
                lineList=f.readlines()
    except Exception as e:
        print "readLineListFromFile:",e
    except:
        print "readLineListFromFile: unknow Exception"  
    return lineList
                      
def  writeLine2File(data):
    global todayShanghaiFile
    try:
        with FileLock("stockdata.txt"):
            with open(todayShanghaiFile,'a') as f:       
                f.write( str(data) )
                f.write('\n')
    except Exception as e:
        print "writeLine2File:",e
    except:
        print "writeLine2File: unknow Exception"  
        
def isChangeTime(): 
    now=datetime.datetime.now()
    if now.hour==9 and now.minute >= 30:
        return True
    if now.hour==11 and now.minute <= 30:
        return True        
    if now.hour==10 or now.hour==13 or now.hour==14:
        return True
    return False          

class FenxiItem1:
    def __init__(self):
        self.name = 'FenxiItem1'     
        self.total = 0    
        self.rise_top = 0 
        self.rise = 0        
        self.fall = 0    
        self.fall_bottom = 0 
        self.keep_zero = 0    
        self.keep_one = 0 
        self.keep_one1=0
        self.zuixinjia = 0.0    
        self.zhangdiefu = 0.0 
        self.zuoshou=0.0
        self.jinkai = 0.0  
        self.zuigao = 0.0  
        self.zuidi = 0.0  
        self.chengjiaoliang = 0.0  
        self.chengjiaoqian = 0.0  
        self.huanshou = 0.0  
        self.zhenfu = 0.0  
        self.liangbi = 0.0  
        self.tm = 0
    def dump(self):     
        tm=getNowHourMinute()
        self.tm=tm
        data1="{0},total:{1},rise:{2},top:{3},fall:{4},bottom:{5},zero:{6},one:{7},one1:{8},zxj:{9},zdf:{10},zs:{11},jk:{12},zg:{13},zd:{14},cjl:{15},cje:{16},hs:{17},zhf:{18},lb:{19}".format(
        tm,self.total,self.rise,self.rise_top,self.fall,self.fall_bottom,self.keep_zero,self.keep_one,self.keep_one1,self.zuixinjia,self.zhangdiefu,self.zuoshou,self.jinkai,self.zuigao,self.zuidi,self.chengjiaoliang,self.chengjiaoqian,self.huanshou,self.zhenfu,self.liangbi)
        data2="{0},total:{1},rise:{2},top:{3},fall:{4},bottom:{5},zero:{6},one:{7},one1:{8},zdf:{9},hs:{10},zhf:{11},lb:{12}".format(
        tm,self.total,self.rise,self.rise_top,self.fall,self.fall_bottom,self.keep_zero,self.keep_one,self.keep_one1,self.zhangdiefu,self.huanshou,self.zhenfu,self.liangbi) 
        print data2
        writeLine2File(data1)                      