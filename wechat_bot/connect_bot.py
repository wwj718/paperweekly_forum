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
logging.basicConfig(filename=LOG_FILE,level=logging.INFO)
logger = logging.getLogger(__name__)
handler=logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
#########




# todo ： group1 和group2硬编码部分抽象为函数
# todo：targetGroupIds = []
group1_id = None
group2_id = None
group1 = 'gtest'
group2 = 'paper测试'
group1_msg_list=[]
group2_msg_list=[]
#paperweeklyGroupName = 'PaperWeekly交流群'




def change_function():
    global group1_msg_list
    global group2_msg_list
    global group1_id
    global group2_id

    #threads = message_tool_use_timestamp.get_threads()
    if  group1_msg_list and group1_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group1_msg_list)
        for msg in group1_msg_list:
            message = '@{}：\n{}'.format(msg['ActualNickName'],msg['Text'])
            itchat.send_msg(message,group2_id) #完成主动推送
        group1_msg_list = []
    if  group2_msg_list and group2_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group2_msg_list)
        for msg in group2_msg_list:
            message = '@{}：\n{}'.format(msg['ActualNickName'],msg['Text'])
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
        if msg['FromUserName'] == group1_id: #针对性处理消息
            print('微信群{}连接完毕'.format(group1))
            #response = handle_group_msg(msg) # type
            # 来自群1消息，加入消息队列
            if '/bot/h' in msg["Text"]:
                response='Hi @{}：\nmessage bot是个信使机器人，将使1、2群消息互通\nhave a nice weekend ：)\n源码已开放：https://github.com/wwj718/paperweekly_forum'.format(msg['ActualNickName'])
                itchat.send_msg(response,group1_id)
            else:
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
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if '/bot/h' in msg["Text"]:
                response='Hi @{}：\nmessage bot是个信使机器人，将使1、2群消息互通\nhave a nice weekend ：)\n源码已开放：https://github.com/wwj718/paperweekly_forum'.format(msg['ActualNickName'])
                itchat.send_msg(response,group2_id)
            else:
                group2_msg_list.append(msg)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logger.info((now,group2,msg['ActualNickName'],msg["Text"]))
        if not group2_id:
            group2_instance = itchat.search_chatrooms(name=group2)
            if group2_instance:
                group2_id = group2_instance[0]['UserName']
                itchat.send_msg('发现{}id，信使机器人已激活: )'.format(group2),group2_id)




itchat.auto_login(enableCmdQR=2,hotReload=True) #调整宽度：enableCmdQR=2
thread.start_new_thread(itchat.run, ())

while 1:
    change_function()
    time.sleep(1)

