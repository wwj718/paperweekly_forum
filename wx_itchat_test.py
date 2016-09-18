#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
# 另一个微信库：https://github.com/littlecodersh/ItChat
import itchat
from itchat.content import TEXT
import ipdb
import redis_client
import redis
#ipdb.set_trace()
import thread
import time
import threading

# 需要在主循环中，有一个轮询机制，而不是回调，目前只能是回调,使用多线程.微信有任何消息，都会查一次 , 需要有一个消息队列, redis
# 发布订阅模型 PubSub

# http://itchat.readthedocs.io/zh/latest/3.Handler/
# https://gist.github.com/jobliz/2596594

# 论坛发往微信
# 如何主动往微信推送


# http://itchat.readthedocs.io/zh/latest/6.Member%20stuff/

'''
# 动态注册到类里
@itchat.msg_register
def simple_reply(msg):
    if msg['Type'] == TEXT:
        print(msg['Content'])
        print itchat.search_chatrooms(name='gtest')

        # 在一次登录中群id不变
        # 好友的UserName每登录一次都会改变
        # msg['ActualNickName'] 就是发送者名字
        # ActualUserName

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    message = '{}:{}'.format(msg['FromUserName'],msg['Content'])
    print(message)
    response = "收到{}：{}".format(msg['FromUserName'],msg['Content'])
    ipdb.set_trace()
    itchat.send(response,msg['FromUserName'])

'''

# 多线程

channels = ['test']
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe(channels)
def change_function():
  #data_list = pubsub.listen()
  #for item in data_list: #会一直等待# The last for section will block,使用多线程,处理阻塞问题
  message = pubsub.get_message()
  if message:
    print message
    # 确实非阻塞，实时性的话，用多线程吧
  # 主动推送
  @itchat.msg_register
  def simple_reply(msg):
      if msg['Type'] == TEXT:
          print(msg['Content'])
          #print itchat.search_chatrooms(name='gtest')
          # 全局存下，在一次登录中不变


# 多线程直接用thread,上下文, 协程



itchat.auto_login()
thread.start_new_thread(itchat.run, ())
#itchat.run()

while 1:
    change_function()
    time.sleep(1)


# https://github.com/Urinx/WeixinBot/issues/68 ,主动推送
