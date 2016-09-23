#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import itchat   # 另一个微信库：https://github.com/littlecodersh/ItChat
from itchat.content import TEXT
#import redis
#ipdb.set_trace()
import thread
import time
import datetime
import re

#########
#log
import logging
LOG_FILE = "/tmp/wechat_log.log"
logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler=logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# 设置一些其他信息 ,时间之类
#########




# 需要在主循环中，有一个轮询机制，而不是回调，目前只能是回调,使用多线程.微信有任何消息，都会查一次 , 需要有一个消息队列, redis
# 发布订阅模型 PubSub

# http://itchat.readthedocs.io/zh/latest/3.Handler/
# https://gist.github.com/jobliz/2596594

# 论坛发往微信
# 如何主动往微信推送

# http://itchat.readthedocs.io/zh/latest/6.Member%20stuff/
# todo：targetGroupIds = []
group1_id = None
group2_id = None
group1 = 'gtest'
group2 = 'paper测试'
group1_msg_list=[]
group2_msg_list=[]
# 内存中村消息列表，发送后清空 ，log存储
#paperweeklyGroupName = 'PaperWeekly交流群'




def change_function():
    global group1_msg_list
    global group2_msg_list
    global group1_id
    global group2_id

    #data_list = pubsub.listen()
    #for item in data_list: # The last for section will block,使用多线程,处理阻塞问题
    # 到kinto上轮询
    #threads = message_tool_use_timestamp.get_threads()
    # 现在没有区帖子,从内存中取信息
    if  group1_msg_list and group1_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group1_msg_list)
        for msg in group1_msg_list:
            message = '来自{} @{}的消息：\n{}'.format(group1,msg['ActualNickName'],msg['Text'])
            itchat.send_msg(message,group2_id) #完成主动推送
        group1_msg_list = []
        #print('主动推送：',threads)
    if  group2_msg_list and group2_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group2_msg_list)
        for msg in group2_msg_list:
            message = '来自{} @{}的消息：\n{}'.format(group2,msg['ActualNickName'],msg['Text'])
            itchat.send_msg(message,group1_id) #完成主动推送
        group2_msg_list = []
    @itchat.msg_register(TEXT, isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        global group1_msg_list
        global group2_msg_list
        global group1_id
        global group2_id
        #itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        # 需要判断是否处理消息，只处理目标群消息
        # 消息来的时候，群入消息队列
        if msg['FromUserName'] == group1_id: #针对性处理消息
            print('微信群{}连接完毕'.format(group1))
            # 业务逻辑 , 回调handle
            #response = handle_group_msg(msg) # type
            # 不需要回掉直接写
            # 来自群1消息，加入消息队列
            group1_msg_list.append(msg)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info((now,group1,msg['ActualNickName'],msg["Text"]))
        if not group1_id:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            group1_instance = itchat.search_chatrooms(name=group1) #本地测试群
            if group1_instance:
                group1_id = group1_instance[0]['UserName']
                itchat.send_msg('发现{}id，信使机器人已激活: )'.format(group1),group1_id)

        if msg['FromUserName'] ==  group2_id:
            print('微信群{}连接完毕'.format(group2))
            # 业务逻辑 , 回调handle
            group2_msg_list.append(msg)
            # datatime
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info((now,group2,msg['ActualNickName'],msg["Text"]))
        if not group2_id:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            group2_instance = itchat.search_chatrooms(name=group2) #本地测试群
            if group2_instance:
                group2_id = group2_instance[0]['UserName']
                itchat.send_msg('发现{}id，信使机器人已激活: )'.format(group2),group2_id)




itchat.auto_login(enableCmdQR=2,hotReload=True) #调整宽度：enableCmdQR=2
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
