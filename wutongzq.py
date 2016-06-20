# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng
import lxml.html
from common import *
from DongtaiRequest import *

class GetWutongZqRequst(DongtaiRequest):
    def __init__(self):
        super(GetWutongZqRequst, self).__init__()
        self.url="http://www.wutongzq.com"
        self.name="wtzq"

    ##############################################
    # overide parseHtml
    #############################################
    def parseHtml(self,html):
        doc = lxml.html.fromstring(html)
        if  doc is  None:
            self.alarm("lxml.html.fromstring error")
            return ""
        numList = doc.xpath('//div[@class="list"]/ul/a/li[@class="right_title"]/text()')
        if  numList is None:
            self.alarm(" numList is Noner")
            return ""
        if len(numList) == 0:
            self.alarm(" len(numList) == 0")
            return ""
        item=numList[0]  
        return item


