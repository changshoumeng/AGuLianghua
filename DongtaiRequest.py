# -*- coding: utf-8 -*-
# Give wisdom to the machine,By ChangShouMeng
import urllib, urllib2, cookielib, socket, time, random
from urllib2 import URLError, HTTPError
import lxml.html
import traceback
import alarmReport
socket.setdefaulttimeout(5)

class DongtaiRequest(object):
    def __init__(self):
        self.url = ""
        self.lastItem = ""
        self.workFailedCount=0
        self.name="DongtaiRequest"

    def doGet(self):
        response = ""
        if len(self.url) <1:
            print "doGet Error url Empty:",self.url
            return
        # httpHandler = urllib2.HTTPHandler(debuglevel=1)
        # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        # opener = urllib2.build_opener(httpHandler, httpsHandler)
        # urllib2.install_opener(opener)
        # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        # request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        try:
            request = urllib2.Request(self.url)
            self.fillHttpRequestHeader(request)
            response = urllib2.urlopen(request, timeout=5)
            page = response.read()
            if page:
                response = page
        except URLError, e:
            if hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request. errorcode:{0}'.format(e.code))
            elif hasattr(e, 'reason'):
                print('We failed to reach a server. reason:{0}'.format(e.reason))
        except:
            print traceback.format_exc()
        return response

    def fillHttpRequestHeader(self,request):
        pass

    def parseHtml(self, html):
        print "DongtaiRequest parseHtml "
        return ""

    def triggerAlarm(self):
        if self.workFailedCount >= 3:
            title = "process error,please check code"
            text = "{0} run failed".format(self.name)
            alarmReport.reportAlarm(title, text)
        else:
            pass

    def alarm(self,text):
        title = self.name
        alarmReport.reportAlarm(title, text)

    def updateItem(self,item):
        if len(item)<1:
            return
        if len(item) == len(self.lastItem) and  item == self.lastItem:
            return
        self.lastItem = item
        print ">>:",self.lastItem
        self.workFailedCount = 0
        self.alarm(self.lastItem)

    def run(self):
        try:
            html = self.doGet();
            if html is None:
                print "run Error: doGet failed"
                self.workFailedCount += 1
                return
            if len(html) < 1:
                print "run Error:", html
                self.workFailedCount += 1
                return
            item = self.parseHtml(html)
            self.updateItem(item)
        except:
            print traceback.format_exc()
            self.workFailedCount += 1
            self.triggerAlarm()