#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import itchat   # 另一个微信库：https://github.com/littlecodersh/ItChat
from itchat.content import TEXT
#import redis
#ipdb.set_trace()
import thread
import time
import forum_client
import re
import message_tool_use_timestamp
# 需要在主循环中，有一个轮询机制，而不是回调，目前只能是回调,使用多线程.微信有任何消息，都会查一次 , 需要有一个消息队列, redis
# 发布订阅模型 PubSub

# http://itchat.readthedocs.io/zh/latest/3.Handler/
# https://gist.github.com/jobliz/2596594

# 论坛发往微信
# 如何主动往微信推送

# http://itchat.readthedocs.io/zh/latest/6.Member%20stuff/
# todo：targetGroupIds = []
paperweeklyGroupId = None #目标群id，每次登陆都不同，同一次登录不变
#paperweeklyGroupName = 'paperweekly bbs' #目标群id，每次登陆都不同，同一次登录不变
paperweeklyGroupName = 'gtest'
#paperweeklyGroupName = 'PaperWeekly交流群'


def handle_group_msg(msg):
    #forum_client.post_thread
    #forum_client.post_reply
    # forum_client.post_reply('wwj','9',u'测试回复.')
    print(msg)
    username = msg['ActualNickName'] # 发言者
    content = msg['Text']
    if '/bot/q' in content:
        clean_content = re.split(r'/bot/q', content)[-1]
        response = forum_client.post_thread(username,clean_content)
        return {'type':'q','response':response}

    # /bot/q 测试第一个问题
    # /bot/t/9 这是帖子9的答复
    if '/bot/t' in content:
        # 正则获取
        thread_id,clean_content = re.split(r'/bot/t/(?P<id>\d+)', content)[-2:]
        response = forum_client.post_reply(username,thread_id,clean_content)
        return {'type':'t','response':response}

    if '/bot/h' in content:
        # 正则获取
        response='paperweekly_bot使用说明：帮助:/bot/h\n发帖:/bot/q 帖子内容\n回帖:/bot/t/(id) 回复内容'

        return {'type':'h','response':response}
    return {'type':None,'response':None}

def change_function():
    global paperweeklyGroupId

    #data_list = pubsub.listen()
    #for item in data_list: # The last for section will block,使用多线程,处理阻塞问题
    # 到kinto上轮询
    threads = message_tool_use_timestamp.get_threads()
    if threads and paperweeklyGroupId:  # 全局变量paperweeklyGroupId ,初始化为None
        print(threads)
        # message是json,data值为序列化后的json数据,需要做反序列化，可以参考test文件
        #print("paperweeklyGroupId:", paperweeklyGroupId)
        # 成功发送
        for item in threads:
            # thread_id,username,title,content
            thread_message = '新的讨论：\n帖子id:{}\n发帖人:{}\n标题:{}\n内容:{}\n论坛地址：http://paperweekly.just4fun.site'.format(item['thread_id'],item['username'],item['title'],item['content'])

            itchat.send_msg(thread_message, paperweeklyGroupId) #完成主动推送
        #print('主动推送：',threads)
    @itchat.msg_register(TEXT, isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        # @
        #itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        # 需要判断是否处理消息，只处理目标群消息
        global paperweeklyGroupId
        if msg['FromUserName'] == paperweeklyGroupId:
            print('处理群gtest消息')
            # 业务逻辑 , 回调handle
            response = handle_group_msg(msg) # type
            print response
            if response['type'] == 'q': # 发送帖子
                pass # 论坛乎触发
                #to_wechat_msg = '帖子发送成功 \n 帖子id：{} \n 使用 /bot/t/(id) 可回复'.format(response['response']['id'])
                #itchat.send_msg(to_wechat_msg, paperweeklyGroupId)

            if response['type'] == 't': #回复帖子
                to_wechat_msg = '帖子回复成功 : )'
                itchat.send_msg(to_wechat_msg, paperweeklyGroupId)
            if response['type'] == 'h': #回复帖子
                to_wechat_msg = response['response']
                itchat.send_msg(to_wechat_msg, paperweeklyGroupId)
            # 做个日志记录
        if not paperweeklyGroupId:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            gtest = itchat.search_chatrooms(name=paperweeklyGroupName) #本地测试群
            if gtest:
                paperweeklyGroupId = gtest[0]['UserName']
                itchat.send_msg('发现群id，微信<=>论坛机器人已激活:)', paperweeklyGroupId)
        #print(msg)
        #print('test:', msg['Content'])
        #print("search_chatrooms:",
        #      itchat.search_chatrooms(name='gtest'))
        # NickName， PYQuanPin(全拼)
        # 消息来自的用户：msg['ActualNickName']
        #print('get_chatrooms:',itchat.get_chatrooms())



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
