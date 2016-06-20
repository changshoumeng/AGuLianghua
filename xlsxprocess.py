#-*-coding:utf-8-*-
import os
import time

from pyExcelerator import *

import xlrd
from xlutils.copy import copy
from stockdesc import *


def getLastMonthDay():
    tt = int(time.time())
    tt = tt - 60*60*24
    return time.strftime("%m=%d", time.localtime(tt))

def getMonthDay():
    return time.strftime("%m=%d",time.localtime(time.time()))

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

def createNewXlsx(fn):
    print "createNewXmls:",fn
    w = Workbook()
    ws = w.add_sheet('data')
    for row in xrange(10000):
        col=0
        ws.write(row, 0, "#")#time
    w.save(fn)

def updateXlsx( code,open,close,high,low,amount,turnover,amplitude,rate,date ):
    try:
        month_day=getMonthDay()
        fn=r"table/{0}.xlsx".format(code)
        if not  os.path.exists(fn):
            createNewXlsx(fn)
            pass
        data = open_excel(fn)
        tmpData = copy(data)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        for row in xrange(nrows):
              col=0
              if   table.row(row)[col].value == month_day:
                  tmpData.get_sheet(0).write(row, 1,open)
                  tmpData.get_sheet(0).write(row, 2, close)
                  tmpData.get_sheet(0).write(row, 3, high)
                  tmpData.get_sheet(0).write(row, 4, low)
                  tmpData.get_sheet(0).write(row, 5, amount)
                  tmpData.get_sheet(0).write(row, 6, turnover)
                  tmpData.get_sheet(0).write(row, 7, amplitude)
                  tmpData.get_sheet(0).write(row, 8, rate)
                  tmpData.get_sheet(0).write(row, 9, date)
                  break
              if   table.row(row)[col].value == "#":
                  tmpData.get_sheet(0).write(row, 0, month_day)
                  tmpData.get_sheet(0).write(row, 1,open)
                  tmpData.get_sheet(0).write(row, 2, close)
                  tmpData.get_sheet(0).write(row, 3, high)
                  tmpData.get_sheet(0).write(row, 4, low)
                  tmpData.get_sheet(0).write(row, 5, amount)
                  tmpData.get_sheet(0).write(row, 6, turnover)
                  tmpData.get_sheet(0).write(row, 7, amplitude)
                  tmpData.get_sheet(0).write(row, 8, rate)
                  tmpData.get_sheet(0).write(row, 9, date)
                  break
        tmpData.save(fn)
    except:
        print "updateXlsx except:",( code,open,close,high,low,amount,turnover,amplitude,rate )
        pass

def getLastAmout( code):
    try:
        month_day= getMonthDay()
        fn=r"table/{0}.xlsx".format(code)
        if not  os.path.exists(fn):
            return None
        data = open_excel(fn)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        for row in xrange(nrows):
              col=0
              if   table.row(row)[col].value == month_day:
                  if row==0:
                      return None
                  open=table.row(row-1)[1].value
                  close = table.row(row - 1)[2].value
                  high = table.row(row - 1)[3].value
                  low = table.row(row - 1)[4].value
                  amount = table.row(row - 1)[5].value
                  turnover = table.row(row - 1)[6].value
                  amplitude = table.row(row - 1)[7].value
                  rate = table.row(row - 1)[8].value
                  return  (open,close,high,low,amount,turnover,amplitude,rate )
              if   table.row(row)[col].value == "#":
                  return None
    except:
        print "getLastAmout:",code
    return  None








'''
inFile= r'table/test.xlsx'
def setNewValue(rowIndex, colIndex, newValue):
    data = xlrd.open_workbook(inFile)
    tmpData = copy(data)
    tmpData.get_sheet(0).write(rowIndex, colIndex, newValue)
    tmpData.save("tmp.xls")

setNewValue(2,0,"11111")

'''


if __name__ == '__main__':
    pass
    #createNewXlsx("002")
    #updateXlsx("0022","11111")
    #updateXlsx("002", "222")
    #updateXlsx("002", "1122111")
    #print  getLastAmout("000001")


