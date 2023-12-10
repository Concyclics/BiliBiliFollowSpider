#CopyRight: Concyclics
# -*- coding:UTF-8 -*-

import sqlite3
import json
import requests

class BiliFollowDB:

    def __init__(self, DBname):
        self.DBname=DBname
        self.link=sqlite3.connect(DBname)
        self.cursor=self.link.cursor()
        
    def __del__(self):
        self.link.commit()
        self.link.close()
        
    def createDB(self):
        self.link=sqlite3.connect(self.DBname)
        self.cursor=self.link.cursor()
        
        print("database open success")
        
        UserTableDDL='''
                    create table if not exists user(
                    UID int PRIMARY KEY     NOT NULL,
                    NAME varchar            NOT NULL,
                    SIGN varchar            DEFAULT NULL,
                    vipType int             NOT NULL,
                    vipDueDate int          DEFAULT NULL,
                    followersTotal int      DEFAULT 0,
                    followingTotal int      DEFAULT 0,
                    followersVerified int     DEFAULT 0,
                    followingVerified int     DEFAULT 0
                    );
                    '''
        
        RelationTableDDL='''
                    create table if not exists relation(
                    follower int           NOT NULL,
                    following int          NOT NULL,
                    followTime int         NOT NULL,
                    PRIMARY KEY (follower, following)
                    );
                    '''
        
        INDEX_RelationTableDDL='''
                    create index if not exists relation_follower on relation(follower);
                    create index if not exists relation_following on relation(following);
                    create index if not exists uid_index on user(UID);
                    '''
        
        # create user table
        self.link.execute(UserTableDDL)
        
        # create relation table
        self.link.execute(RelationTableDDL)
        
        print("database create success")
        
        self.link.commit()

    def commit(self):
        self.link.commit()

    def addNewUser(self, info):
        InsertCmd="insert into user (UID, NAME, SIGN, vipType, vipDueDate) values (?,?,?,?,?);"

        self.cursor.execute(InsertCmd,(info['uid'], info['name'], info['sign'], info['vipType'], info['vipDueDate']))

    def UpdateUser(self, info):
        UpdateCmd="update user set NAME=?, SIGN=?, vipType=?, vipDueDate=?, followersTotal=?, followingTotal=? where UID=?;"

        self.cursor.execute(UpdateCmd,(info['name'], info['sign'], info['vipType'], info['vipDueDate'], info['followersTotal'], info['followingTotal'], info['uid']))
        self.link.commit()

    def UpdateUserFollowers(self, uid, followersTotal):
        UpdateCmd="update user set followersTotal=? where UID=?;"

        self.cursor.execute(UpdateCmd,(followersTotal, uid))
        self.link.commit()

    def UpdateUserFollowing(self, uid, followingTotal):
        UpdateCmd="update user set followingTotal=? where UID=?;"

        self.cursor.execute(UpdateCmd,(followingTotal, uid))
        self.link.commit()
    
    def addNewRelation(self, follower, following, followTime):
        InsertCmd="insert into relation (follower, following, followTime) values (?,?,?);"
        incrementFollowerCmd="update user set followersVerified=followersVerified+1 where UID=%d;" % following
        incrementFollowingCmd="update user set followingVerified=followingVerified+1 where UID=%d;" % follower

        self.cursor.execute(InsertCmd, (follower, following, followTime))
        self.cursor.execute(incrementFollowerCmd)
        self.cursor.execute(incrementFollowingCmd)

    def getExistingUID(self):
        SelectCmd="select UID from user;"

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append(row[0])
        return IDs
    
    def getExistingUIDAndName(self):
        SelectCmd="select UID, NAME from user;"

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append({'UID':row[0], 'NAME':row[1]})
        return IDs
    
    def getNameByUID(self, uid):
        SelectCmd="select NAME from user where UID=%d;" % uid

        answer=self.cursor.execute(SelectCmd)
        for row in answer:
            return row[0]
        return None
    
    def getExistingUserAndFollowCount(self):
        SelectCmd="select UID, followersTotal, followingTotal, followersVerified, followingVerified from user;"

        answer=self.cursor.execute(SelectCmd)
        Users=[]
        for row in answer:
            Users.append({'UID':row[0], 'followersTotal':row[1], 'followingTotal':row[2], 'followersVerified':row[3], 'followingVerified':row[4]})
        return Users
    
    def getFollowingUIDs(self, uid):
        SelectCmd="select following from relation where follower=%d;" % uid

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append(row[0])
        return IDs
    
    def getFollowerUIDs(self, uid):
        SelectCmd="select follower from relation where following=%d;" % uid

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append(row[0])
        return IDs
    
    def getFollowingUIDsAndTime(self, uid):
        SelectCmd="select following, followTime from relation where follower=%d;" % uid

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append({'UID':row[0], 'followTime':row[1]})
        return IDs
    
    def getFollowerUIDsAndTime(self, uid):
        SelectCmd="select follower, followTime from relation where following=%d;" % uid

        answer=self.cursor.execute(SelectCmd)
        IDs=[]
        for row in answer:
            IDs.append({'UID':row[0], 'followTime':row[1]})
        return IDs
    

        
    

