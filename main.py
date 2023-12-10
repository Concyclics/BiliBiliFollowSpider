#CopyRight: Concyclics
# -*- coding:UTF-8 -*-

import os
from BiliFollowSpider import BiliFollowSpider

config={
    'DBname': "BiliFollow.db", #数据库名
    'coldstart': True, #是否初次启动
    'initUID': 208259, #初次启动时的起点UID
    'facePath': 'face/', #头像存储路径
    'cookie': "Put your cookie here" #登录cookie
    }

if __name__ == "__main__":
    spider=BiliFollowSpider(config['DBname'], config['cookie'], config['facePath'])
    spider.updateCookie(config['cookie'])
    if config['coldstart']:
        spider.coldstart(config['initUID'])
    else:
        spider.warmstart()

    