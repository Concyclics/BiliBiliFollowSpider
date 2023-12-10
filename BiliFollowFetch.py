#CopyRight: Concyclics
# -*- coding:UTF-8 -*-

import sqlite3
import json
import requests

class BiliFollowFetch:
    
    def __init__(self):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Cookie':"666"
            }
    
    def __del__(self):
        pass

    def updateCookie(self, cookie:str):
        self.headers['Cookie']=cookie
    
    def getFollowingList_work(self, uid:int, page:int):
    
        url="https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d"# % (UID, Page Number)

        html=requests.get(url%(uid, page), headers=self.headers)
        if html.status_code!=200:
            print("GET ERROR for user %d!"%uid)
            return False
            
        text=html.text
        dic=json.loads(text)
        
        if dic['code']!=0:
            print("access denied for user %d"%uid)
            return False

        try:
            List=dic['data']['list']
            total=int(dic['data']['total'])
        except:
            print("extract error for user %d"%uid)
            return False
        
        if len(List)==0:
            print("no following for user %d"%uid)
            return False
        
        return List, total

    def getFollowersList_work(self, uid:int, page:int):

        url="https://api.bilibili.com/x/relation/followers?vmid=%d&pn=%d"# % (UID, Page Number)

        html=requests.get(url%(uid, page), headers=self.headers)
        if html.status_code!=200:
            print("GET ERROR for user %d!"%uid)
            return False
            
        text=html.text
        dic=json.loads(text)
        
        if dic['code']!=0:
            print("access denied for user %d"%uid)
            return False

        try:
            List=dic['data']['list']
            total=int(dic['data']['total'])
        except:
            print("extract error for user %d"%uid)
            return False
        
        return List, total
    
    def getFollowingList(self, uid:int):
        page=1
        totalList=[]
        total=0
        
        while True:
            result=self.getFollowingList_work(uid, page)
            if result==False:
                break
            List, total=result
            totalList+=List
            page+=1

        if len(totalList)==0:
            print("no following for user %d"%uid)
            return False
        
        return totalList, total
    
    def getFollowersList(self, uid:int):
        page=1
        totalList=[]
        total=0
        
        while True:
            result=self.getFollowersList_work(uid, page)
            if result==False:
                break
            List, total=result
            totalList+=List
            page+=1

        if len(totalList)==0:
            print("no following for user %d"%uid)
            return False
        
        return totalList, total
    
if __name__ == "__main__":
    Spider=BiliFollowFetch()
    data, total=Spider.getFollowingList(8271556)
    print(total)

    
    
    