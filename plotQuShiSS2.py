# -*- coding: utf-8 -*-
 
import time
import matplotlib.pyplot as plt
import numpy as np
import threading
import Queue
import random
from matplotlib.dates import datetime
from matplotlib.widgets import Cursor
from filelock import FileLock
from common import * 


timer_seconds=10
last_minute=0
myqueue = Queue.Queue(maxsize =0)   
event=threading.Event()
event.set()
max_y=100 
tick_count=300
max_x=tick_count

##############################################
##autolabel
##############################################      
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % float(height))    


##############################################
##autolabel
############################################## 
#plt.figure(figsize=(8,7),dpi=98)
#plt.figure()
fig, ax = plt.subplots()
ind = np.arange(0,tick_count)
bars=plt.bar(ind, [0]*tick_count,width=0.7,yerr=0.000001)
#plt.legend(bars,(u"图例",))

ax.set_xlim([0, tick_count])
ax.set_ylim([0, max_y])

ax.set_yticks(range(0,max_y,5))
ax.set_xticks(range(0,tick_count,10))

ax.set_ylabel('Percent usage')
ax.set_xlabel('time tick')
ax.set_title('System Monitor')

cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
plt.show(block=False)
plt.grid(True)
#autolabel(bars)
 

##############################################
##parseLine
############################################## 
def parseLine(line):
    item=FenxiItem1()
    a=line.split(',')
    item.tm  = a[0]
    rise=a[2]
    #print rise
    rise=rise[5:]
    item.rise=float(rise)
    
    total=a[1]
    total=total[6:]
    item.total=float(total)
    
    item.rise_percent=item.rise *100/item.total
   
    return item

##############################################
##findMountaintop
##############################################     
def findMountaintop(y_val_list,begin,end):      
    top=[]
    bottom=[]
    i=begin  
    lastEnd=0
    last_max_val=0
    last_min_val=0
    while i<end:       
       chunkSize=min( end-i,5 )
       lastEnd=i+chunkSize
       chunk=y_val_list[i:lastEnd]       
       max_val=max(chunk)
       min_val=min(chunk) 
       if True:
           max_i1=0
           if last_max_val != 0:
               max_i1=y_val_list.index(last_max_val)
           max_i2=chunk.index(max_val)+i
           
           #top.append( max_i1 )
           top.append( max_i2 )
           last_max_val=max_val
           min_i1=0
           if last_min_val != 0:
               min_i1=y_val_list.index(last_min_val)
           min_i2=chunk.index(min_val)+i
           #bottom.append( min_i1 )
           bottom.append( min_i2 )
           last_min_val=min_val
           
       i=lastEnd    
    #print top        
    return [top,bottom]

 

##############################################
##drawLine
##############################################  
def drawLine(y_val_list):   
    count=len(y_val_list)
    if count<10:
        return
    if count%10 !=0 :
        return
        
    begin=drawLine.last_end
    end=count
    [xtop,xbottom]=findMountaintop(y_val_list,begin,end)
    if len(xtop)<=0:
        return
    #print xtop,xbottom
    ytop=[]
    yy=0
    for xx in xtop:
        yy=y_val_list[xx]
        ytop.append(yy)
    #xtop.append(tick_count)   
    #ytop.append(yy)
    plt.plot(xtop,ytop,color='y')   
    
    ybottom=[]
    for xx in xbottom:
        yy=y_val_list[xx]
        ybottom.append(yy)
    plt.plot(xbottom,ybottom,color='r')    
    drawLine.last_end ==end

##############################################
##update
##############################################      
drawLine.last_end=0
y_val_list=[]
lastIndex=0
def update(item):    
    global bars
    global lastIndex    
    global tick_count
    title="{0} rise:{1}".format(item.tm,item.rise)
    ax.set_title(title)  
    print "update [{0}] time:{1} lastIndex:{2} rise:{3}".format(GetNowTime(),item.tm,lastIndex,item.rise)
    if lastIndex > tick_count:
        print "tick count finished,update stop"
        return     
    n=int(item.rise_percent)    
    n=min(100,n)
    for i in xrange(lastIndex):
        bars[i].set_facecolor('g')
        if i >=lastIndex-3:
            bars[i].set_facecolor('b')
    i = lastIndex    
    bars[i].set_height(n)
    bars[i].set_facecolor('r')
    y_val_list.append(n)
    drawLine(y_val_list)
    lastIndex += 1    
    return
##############################################
##initBars
##############################################    
def initBars():
    global last_minute
    lineList=readLineListFromFile() 
    #lineList=lineList[-10:]    
    for line in lineList:
        line=line.strip()
        item=parseLine(line)
        tm=getNowMinuteIntVal(item.tm)       
        if last_minute == 0:
            last_minute = tm
            ax.set_xlabel(item.tm)
        elif  tm >= last_minute+1:            
            last_minute = tm        
            update(item)
            
##############################################
##自动刷新数据
##############################################               
      
def func():
    global myqueue   
    global lastIndex  
    global timer_seconds
    global last_minute
    
    line=readLastLineFromFile()    
    if len(line) > 0 :        
        line=line.strip()
        item=parseLine(line)        
        tm=getNowMinuteIntVal(item.tm)        
        if last_minute == 0:
            last_minute = tm
        elif  tm >= last_minute+1:        
            myqueue.put(item)   
            last_minute = tm  
    if lastIndex>=tick_count:
        print "tick count finished,timer stop"
        return   
    timer = threading.Timer(timer_seconds, func)
    timer.start()   

def startTimer():
    timer = threading.Timer(5, func)
    timer.start()                

if __name__=="__main__":  
    initBars()
    startTimer()    
    ##############################################
    ##自动刷新数据
    ##############################################
    while True:        
        if lastIndex>=tick_count:
            print "tick count finished"
            break
        try:
            item = myqueue.get(timeout=0.2)
            if item==None:
                pass
            else:
                update(item)
        except:
            pass          
        
        try:
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
        except NotImplementedError:
            pass
        

  
    