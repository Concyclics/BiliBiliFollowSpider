#CopyRight: Concyclics
# -*- coding:UTF-8 -*-


import sqlite3
import json
import requests
import os
import queue
from tqdm import tqdm
from BiliFollowDB import BiliFollowDB
from BiliFollowFetch import BiliFollowFetch

class BiliFollowSpider:
    def __init__(self, DBname:str, cookie:str, facePath:str):
        self.DBname=DBname
        self.cookie=cookie
        self.facePath=facePath
        self.existingUserList=set()
        self.Queue=queue.Queue()

        self.db=BiliFollowDB(self.DBname)
        self.spider=BiliFollowFetch()
        self.spider.updateCookie(self.cookie)

        if not os.path.exists(self.facePath):
            os.mkdir(self.facePath)

    def __del__(self):
        pass

    def updateCookie(self, cookie:str):
        self.cookie=cookie
        self.spider.updateCookie(cookie)

    def downloadFace(self, face:str, uid:int):
        faceName = str(uid)+'.jpg'
        facePath = self.facePath+faceName
        if not os.path.exists(facePath):
            html = requests.get(face)
            with open(facePath, 'wb') as f:
                f.write(html.content)
        

    def addaUser(self, User:dict):
        uid = User['mid']
        if uid in self.existingUserList:
            return False
        self.existingUserList.add(uid)
        info = dict()
        info['uid'] = uid
        info['name'] = User['uname']
        info['sign'] = User['sign']
        info['vipType'] = User['vip']['vipType']
        info['vipDueDate'] = User['vip']['vipDueDate']
        face = User['face']

        self.db.addNewUser(info)
        self.downloadFace(face, uid)

        self.Queue.put(uid)
        return True

    def updateFollowing(self, uid:int):
        followingRsult = self.spider.getFollowingList(uid)
        followingExist = set(self.db.getFollowingUIDs(uid))
        if followingRsult != False:
            followingList, total = followingRsult
            self.db.UpdateUserFollowing(uid, total)
            for item in tqdm(followingList):
                newUid = item['mid']
                if newUid not in followingExist:
                    self.db.addNewRelation(uid, newUid, item['mtime'])
                    self.addaUser(item)

        
    def updateFollowers(self, uid:int):
        followersRsult = self.spider.getFollowersList(uid)
        followersExist = set(self.db.getFollowerUIDs(uid))
        if followersRsult != False:
            followersList, total = followersRsult
            self.db.UpdateUserFollowers(uid, total)
            for item in tqdm(followersList):
                newUid = item['mid']
                if newUid not in followersExist:
                    self.db.addNewRelation(newUid, uid, item['mtime'])
                    self.addaUser(item)

    def updateRelation(self, uid:int):
        self.updateFollowing(uid)
        self.updateFollowers(uid)

    def update(self):
        while not self.Queue.empty():
            uid=self.Queue.get()
            self.updateRelation(uid)
            self.db.commit()
            print("update user %d"%uid)

    def warmstart(self):
        userinfos=self.db.getExistingUserAndFollowCount()
        for user in userinfos:
            self.existingUserList.add(user['UID'])
            if (user['followingTotal'] > 0 and user['followingVerified'] < user['followingTotal']) or (user['followersTotal'] > 0 and user['followersVerified'] < user['followersTotal']):
                self.Queue.put(user['UID'])
            elif user['followingTotal'] == 0 and user['followersTotal'] == 0:
                self.Queue.put(user['UID'])

        self.update()

    def coldstart(self, initUID:int):
        self.db.createDB()
        uid=initUID
        followingRsult = self.spider.getFollowingList(uid)
        if followingRsult != False:
            followingList, total = followingRsult
            for item in followingList:
                self.addaUser(item)
                self.updateRelation(item['mid'])

        self.update()





                