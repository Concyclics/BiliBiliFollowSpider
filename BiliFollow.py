#by concyclics
# -*- coding:UTF-8 -*-

import sqlite3
import json
import requests

def createDB():

    link=sqlite3.connect('BiliFollowDB.db')
    
    print("database open success")
    
    UserTableDDL='''
                create table if not exists user(
                UID int PRIMARY KEY     NOT NULL,
                NAME varchar            NOT NULL,
                SIGN varchar            DEFAULT NULL,
                vipType int             NOT NULL,
                verifyType int          NOT NULL,
                verifyDesc varchar      DEFAULT NULL)
                '''
    
    RelationTableDDL='''
                create table if not exists relation(
                follower int           NOT NULL,
                following int          NOT NULL,
                followTime int         NOT NULL,
                PRIMARY KEY (follower,following),
                FOREIGN KEY(follower,following) REFERENCES user(UID,UID)
                )
                '''
    
    # create user table
    link.execute(UserTableDDL)
    
    # create relation table
    link.execute(RelationTableDDL)
    
    print("database create success")
    
    link.commit()
    link.close()
    

def insertUser(infos):
    
    conn=sqlite3.connect('BiliFollowDB.db')
    link=conn.cursor()
    
    InsertCmd="insert into user (UID,NAME,vipType,verifyType,sign,verifyDesc) values (?,?,?,?,?,?);"
    
    ExistCmd="select count(UID) from user where UID='%d';"# % UID
    
    newID=[]
    
    for info in infos:
        answer=link.execute(ExistCmd%info['uid'])
        for row in answer:
            exist_ID=row[0]
        
        if exist_ID==0:
            newID.append(info['uid'])
            link.execute(InsertCmd,(info['uid'],info['name'],info['vipType'],info['verifyType'],info['sign'],info['verifyDesc']))
            
    conn.commit()
    conn.close()
    
    return newID



def insertFollowing(uid:int,subscribe):
    
    conn=sqlite3.connect('BiliFollowDB.db')
    link=conn.cursor()
    
    InsertCmd="insert into relation (follower,following,followTime) values (?,?,?);"
    
    for follow in subscribe:
        try:
            link.execute(InsertCmd,(uid,follow[0],follow[1]))
        except:
            print((uid,follow[0],follow[1]))
        
    conn.commit()
    conn.close()
    
    
    
def getFollowingList(uid:int):
    
    url="https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d&ps=50&order=desc&order_type=attention&jsonp=jsonp"# % (UID, Page Number)
    
    infos=[]
    
    subscribe=[]
    
    for i in range(1,6):
        html=requests.get(url%(uid,i))
        if html.status_code!=200:
            print("GET ERROR!")
            return []
            
        text=html.text
        dic=json.loads(text)
        
        if dic['code']==-400:
            return []
    
        try:
            list=dic['data']['list']
        except:
            return []
        
        for usr in list:
            info={}
            info['uid']=usr['mid']
            info['name']=usr['uname']
            info['vipType']=usr['vip']['vipType']
            info['verifyType']=usr['official_verify']['type']
            info['sign']=usr['sign']
            if info['verifyType']==-1:
                info['verifyDesc']='NULL'
            else :
                info['verifyDesc']=usr['official_verify']['desc']
            
            subscribe.append((usr['mid'],usr['mtime']))
            infos.append(info)
        
    newID=insertUser(infos)
    insertFollowing(uid,subscribe)
    
    return newID

def getFollowingUid(uid:int):
    url="https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d&ps=50&order=desc&order_type=attention&jsonp=jsonp"# % (UID, Page Number)
    
    for i in range(1,6):
        html=requests.get(url%(uid,i))
        if html.status_code!=200:
            print("GET ERROR!")
            return []
        
        text=html.text
        dic=json.loads(text)
        
        if dic['code']==-400:
            return []
        
        try:
            list=dic['data']['list']
        except:
            return []
        
        IDs=[]
        
        for usr in list:
            IDs.append(usr['mid'])

        return IDs

def work(root):
    
    IDlist=root
    tmplist=[]
    while len(IDlist)!=0:
        tmplist=[]
        for ID in IDlist:
            print(ID)
            tmplist+=getFollowingList(ID)
            
        IDlist=tmplist
        
def rework():
    conn=sqlite3.connect('BiliFollowDB.db')
    link=conn.cursor()
    
    SelectCmd="select uid from user;"
    
    answer=link.execute(SelectCmd)
    
    IDs=[]
    
    for row in answer:
        IDs.append(row[0])
        
    conn.commit()
    conn.close()
    
    newID=[]
    
    print(IDs)
        
    for ID in IDs:
        ids=getFollowingUid(ID)
        for id in ids:
            if id not in IDs:
                newID.append(id)
    
    return newID

    

if __name__=="__main__":

    createDB()
    
    #work([**put root UID here**,])
    
    
    
