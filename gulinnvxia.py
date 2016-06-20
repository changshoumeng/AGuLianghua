# -*- coding: utf-8 -*-
# Give wisdom to the machine,By ChangShouMeng
#response.read()#.decode("unicode-escape")
import lxml.html
from DongtaiRequest import *
import json


class GulinnvxiaWeiboRequest(DongtaiRequest):
    def __init__(self):
        super(GulinnvxiaWeiboRequest, self).__init__()
        self.url = "http://m.weibo.cn/u/5091912327A"
        self.name="GuLinNvXia"
    '''
    GET /page/tpl?containerid=1005055091912327_-_WEIBO_SECOND_PROFILE_WEIBO&itemid=&title=%E5%85%A8%E9%83%A8%E5%BE%AE%E5%8D%9A HTTP/1.1
Host: m.weibo.cn
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://m.weibo.cn/u/5091912327
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
Cookie: _T_WM=673b3024c23211658bf9c6fb0ecdd26c; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFyc63FzPwGJAKbFKlZL73k5JpX5o2p5NHD95Q01K5XS0.feoz4Ws4DqcjGBgUfBcyydntt; SUB=_2A256ZVyUDeTxGeVH61YW-SvOyTWIHXVZpmTcrDV6PUJbkdBeLRH2kW0M01dvlnszzCIQODmoIuAeKkkMJQ..; SUHB=0u5RRg_XnTy94F; SSOLoginState=1465986244; gsid_CTandWM=4u4ACpOz5Ok2vFF2s1upHgnOz3H; H5_INDEX=3; H5_INDEX_TITLE=AguChan; M_WEIBOCN_PARAMS=featurecode%3D20000181%26oid%3D3982218961749387%26luicode%3D10000012%26lfid%3D1005055091912327_-_WEIBO_SECOND_PROFILE_WEIBO%26fid%3D1005055091912327_-_WEIBO_SECOND_PROFILE_WEIBO%26uicode%3D10000012
    '''
    def fillHttpRequestHeader(self,request):
        #request = urllib2.Request(self.url)
        request.add_header('Connection', 'keep-alive')
        request.add_header('Cache-Control', 'max-age=0')
        request.add_header('Upgrade-Insecure-Requests', '1')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
       # request.add_header('Referer', 'http://m.weibo.cn/u/5091912327')
       # request.add_header('Accept-Encoding', 'gzip, deflate, sdch')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
        request.add_header('Cookie', '_T_WM=673b3024c23211658bf9c6fb0ecdd26c; gsid_CTandWM=4uwqCpOz5R2NVT24cXJzCgnOz3H; ALF=1468720744; SUB=_2A256ZykjDeTxGeVH61YW-SvOyTWIHXVZq7drrDV6PUJbktBeLUbakW023aMMg3RqugmbbnIg-NZV4jTzVw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFyc63FzPwGJAKbFKlZL73k5JpX5o2p5NHD95Q01K5XS0.feoz4Ws4DqcjGBgUfBcyydntt; SUHB=010Gvr9mvXmAWi; SSOLoginState=1466128756; H5_INDEX=0_all; H5_INDEX_TITLE=AguChan; M_WEIBOCN_PARAMS=featurecode%3D20000181%26fid%3D1005055091912327%26uicode%3D10000011')
        pass

    def parseHtml(self, html):
        print "paseHtml:",html
        doc = lxml.html.fromstring(html)
        numList = doc.xpath('//body/script[contains(text(),"window.$render_data")]/text()')
        if numList is None:
            return ""
        if len(numList) == 0:
            return ""

        item = numList[0]
        pos= item.find('window.$render_data')
        item=item[pos+22:-1]
        s=item
        s = item.replace( "'stage'" , '"stage" ')
        s = s.replace("'page'", '"page" ')
        s = s.replace("'common'", '"common" ')
        try:
            j = json.loads(s)
            for item in j["stage"]["page"]:
                if item["mod_type"] !=  "mod/pagelist":
                    continue
                for i in xrange(5):
                    if item["card_group"][i]["mblog"]["mblogtype"] != 0:
                        continue
                    return  item["card_group"][i]["mblog"]["text"]
        except:
            print "except"
        return ""

def main():
    request = GulinnvxiaWeiboRequest()
    request.run()
    #s='\u6d77\u5916'
    #s='\u6d77\u5916'
    #s=u'你好'
    # s.decode("unicode-escape")
    #print eval(s)

    pass


if __name__ == "__main__":
    main()
