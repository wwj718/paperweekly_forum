#!/usr/bin/env python
# encoding: utf-8

# 构建一个用户模型
# 消息来得时候构建用户
from tinydb import TinyDB, where,Query
import time

class LocalUserTool(object):
    '''
    数据库作为类属性
    是一个工具类
    实质上是数据存储/检索类
    '''
    DB = TinyDB("localuser"+".json")
    # 删掉旧的
    #TABLE= DB.table("localuser"+str(int(time.time()))) # 加上时间戳
    DB.purge_tables() # 移除所有表格
    TABLE= DB.table("localuser") # 加上时间戳

    def __init__(self):
        """TODO: to be defined1.
        :userid: TODO
        """
        pass
    def get_actual_user_name(self,at_id):
        '''
        根据at_id获取用户昵称 ， 用于at
        '''
        #userid = msg["ActualUserName"] # 用户在群里的名字 , 可at
        Record = Query()
        localuser = self.TABLE.get(Record.at_id==at_id) # dict
        if localuser:
            return localuser.get("actual_user_name")
    def get_at_id(self,actual_user_name):
        Record = Query()
        localuser = self.TABLE.get(Record.actual_user_name == actual_user_name) # dict
        if localuser:
            return localuser.get("at_id")
    def set_at_id(self,actual_user_name,groupid=None):
        '''
        设置用户at_id
        '''
        #检验msg["ActualUserName"]是够已分配at_id，如果没有则分配，如果有则
        #new_record["actual_user_name"] = userid
        localuser = {}
        localuser["actual_user_name"] = actual_user_name
        localuser["groupid"] = groupid
        localuser["at_id"] = len(self.TABLE.all())+1 # 自增,从1开始
        self.TABLE.insert(localuser)
        return  localuser["at_id"]
        # 获取用户信息，如果存在则获取，不存在则添加

def main():
    localuser_tool = LocalUserTool()
    print(localuser_tool.get_actual_user_name(10))
    at_id = localuser_tool.get_at_id("@abc")
    if not at_id:
        localuser_tool.set_at_id("@abc")
    at_id = localuser_tool.get_at_id("@abc")
    print(localuser_tool.get_actual_user_name(at_id))


if __name__ == '__main__':
    main()
