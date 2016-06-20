# -*- coding: utf-8 -*-
#Give wisdom to the machine,By ChangShouMeng
import threading
from wutongzq import *
from gulinnvxia import *

getGulinnvxiaWeiboRequest = GulinnvxiaWeiboRequest()


def onceWork():
    getGulinnvxiaWeiboRequest.run()

def func():
    onceWork()
    timer = threading.Timer(10, func)
    timer.start()

def startTimer():
    timer = threading.Timer(1, func)
    timer.start()

if __name__ == "__main__":
    print __file__
    onceWork()
    startTimer()
