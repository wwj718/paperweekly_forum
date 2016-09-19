#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import itchat   # 另一个微信库：https://github.com/littlecodersh/ItChat
from itchat.content import TEXT
import redis
#ipdb.set_trace()
import thread
import time

# 需要在主循环中，有一个轮询机制，而不是回调，目前只能是回调,使用多线程.微信有任何消息，都会查一次 , 需要有一个消息队列, redis
# 发布订阅模型 PubSub

# http://itchat.readthedocs.io/zh/latest/3.Handler/
# https://gist.github.com/jobliz/2596594

# 论坛发往微信
# 如何主动往微信推送

# http://itchat.readthedocs.io/zh/latest/6.Member%20stuff/
# todo：targetGroupIds = []
paperweeklyGroupId = None #目标群id，每次登陆都不同，同一次登录不变
paperweeklyGroupName = 'gtest' #目标群id，每次登陆都不同，同一次登录不变

# redis
channels = ['test'] # redis订阅频道
r = redis.Redis() #sub端要先跑起来
pubsub = r.pubsub()
pubsub.subscribe(channels)


def change_function():
    global paperweeklyGroupId

    #data_list = pubsub.listen()
    #for item in data_list: # The last for section will block,使用多线程,处理阻塞问题
    message = pubsub.get_message() #每次只获取一条
    if message and paperweeklyGroupId:  # 全局变量paperweeklyGroupId ,初始化为None
        # message是json,data值为序列化后的json数据,需要做反序列化，可以参考test文件
        print("paperweeklyGroupId:", paperweeklyGroupId)
        itchat.send_msg(str(message), paperweeklyGroupId) #完成主动推送
        print('主动推送：', message)
    @itchat.msg_register(TEXT, isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        # 需要判断是否处理消息，只处理目标群消息
        global paperweeklyGroupId
        if msg['FromUserName'] == paperweeklyGroupId:
            print('处理群gtest消息')
            # 业务逻辑 , 回调handle
            # 做个日志记录
        if not paperweeklyGroupId:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            gtest = itchat.search_chatrooms(name=paperweeklyGroupName) #本地测试群
            if gtest:
                paperweeklyGroupId = gtest[0]['UserName']
                itchat.send_msg('找到群id:', paperweeklyGroupId)
        #print(msg)
        #print('test:', msg['Content'])
        #print("search_chatrooms:",
        #      itchat.search_chatrooms(name='gtest'))
        # NickName， PYQuanPin(全拼)
        # 消息来自的用户：msg['ActualNickName']
        #print('get_chatrooms:',itchat.get_chatrooms())



itchat.auto_login()
thread.start_new_thread(itchat.run, ())
# 多线程,线程共享了内存，可以考虑协程
# 当前代码是主线程
# thread模块的start_new_thread方法，在线程中运行一个函数，但获得函数返回值极为困难，Python官方不推荐
#itchat.run()

while 1:
    change_function()
    time.sleep(1)

# https://github.com/Urinx/WeixinBot/issues/68 ,主动推送
# https://github.com/Urinx/WeixinBot/blob/da0b2ff1995db97fa7233693cd42ec697785c58d/weixin.py#L300
