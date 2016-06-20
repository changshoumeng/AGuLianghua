# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng
from common import *
from DongtaiRequest import *
import json

class GetTonghuashunRequst(DongtaiRequest):
    def __init__(self):
        super(GetTonghuashunRequst, self).__init__()
        self.url="http://flashcms.10jqka.com.cn/compiled/gundong/v1/1.json"
        self.name = "ghs"

    def parseHtml(self,html):         
        info=""
        try:
            js=json.loads(html) 
            for item in js['pageItems']:
                info= item['title']+"("+item['source']+")"+item['digest']
                break
        except:
            self.alarm(" json.loads Error")
        return info


