#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import itchat   # 另一个微信库：https://github.com/littlecodersh/ItChat
from itchat.content import TEXT,PICTURE,RECORDING, ATTACHMENT, VIDEO,SHARING
#import redis
#ipdb.set_trace()
import thread
import time
import datetime
import re
import message_tool_use_timestamp
import forum_client
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

import qa_bot


# todo ： group1 和group2硬编码部分抽象为函数
# todo：targetGroupIds = []
group1_id = None
group2_id = None
group1 = 'gtest'
group2 = 'paper测试'
#group2 = 'paperweekly bbs'
group1_msg_list=[]
group2_msg_list=[]
#group1 = 'PaperWeekly交流群'
#group2 = 'PaperWeekly交流二群'


def sync_thread():
    # 没有被执行
    print('begin sync_thread')
    global group1_id
    global group2_id
    threads = message_tool_use_timestamp.get_threads()
    print("threads:",threads)
    print("ids:",group1_id,group2_id)
    if threads and group1_id:
        for item in threads:
            # url
            thread_message = '新的讨论：\n帖子id:{}\n发帖人:{}\n标题:{}\n内容:{}\n论坛地址：http://paperweekly.club{}'.format(item['thread_id'],item['username'],item['title'],item['content'],item['url'])
            itchat.send_msg(thread_message,group1_id) #主动推送
    if threads and group2_id:
        for item in threads:
            thread_message = '新的讨论：\n帖子id:{}\n发帖人:{}\n标题:{}\n内容:{}\n论坛地址：http://paperweekly.club{}'.format(item['thread_id'],item['username'],item['title'],item['content'],item['url'])
            itchat.send_msg(thread_message,group2_id)
    print('end sync_thread')


def change_function():
    print("begin change_function")
    global group1_msg_list
    global group2_msg_list
    global group1_id
    global group2_id

    sync_thread()
    # get thread and post it ,同步帖子
    #sync_thread() #todo:单独作为线程
    if  group1_msg_list and group1_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group1_msg_list)
        # 可以不需要队列，直接发送即可，考虑到3个群的问题
        for msg in group1_msg_list:
            message = '@{}发言：\n{}'.format(msg['ActualNickName'],msg['Text'])
            itchat.send_msg(message,group2_id) #完成主动推送
            group1_msg_list.remove(msg)
    if  group2_msg_list and group2_id:  # 全局变量paperweeklyGroupId ,初始化为None
        print(group2_msg_list)
        for msg in group2_msg_list:
            message = '@{}发言：\n{}'.format(msg['ActualNickName'],msg['Text'])
            itchat.send_msg(message,group1_id) #完成主动推送
            group2_msg_list.remove(msg)
    @itchat.msg_register([TEXT,SHARING,PICTURE], isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        global group1_msg_list
        global group2_msg_list
        global group1_id
        global group2_id
        #itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        # 需要判断是否处理消息，只处理目标群消息
        print("simple_reply begin msg")
        if msg['FromUserName'] == group1_id: #针对性处理消息
          print('微信群{}连接完毕'.format(group1))
          print(msg)
          #response = handle_group_msg(msg) # type
          # 来自群1消息，加入消息队列
          #if '/bot' in msg["Text"] or '[疑问]' in msg["Text"]:
          # 多一个分支，if msg["Type"] == 'Picture'
          if msg["Type"] == 'Text':
            if msg["Text"].startswith('[疑问]') or msg["Text"].startswith('[闭嘴]') or  msg["Text"].startswith('[得意]') or  msg["Text"].startswith('[惊讶]'):
                # 这些是系统功能不转发
                response = handle_group_msg(msg) # type
                if response['type'] == 'q': # 发送帖子
                    pass # 论坛会触发到两个群
                if response['type'] == 'qa': # 发送帖子
                    to_wechat_msg = response['response']
                    itchat.send_msg(to_wechat_msg,group1_id)

                if response['type'] == 't': #回复帖子
                    to_wechat_msg = '@{} 帖子回复成功 : )'.format(msg['ActualNickName'])
                    itchat.send_msg(to_wechat_msg,group1_id)
                if response['type'] == 'h': #回复帖子
                    to_wechat_msg = response['response']
                    itchat.send_msg(to_wechat_msg,group1_id)
            else:
                    #普通文本消息
                    group1_msg_list.append(msg)
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logger.info((now,group1,msg['ActualNickName'],msg["Text"]))
          if msg["Type"] == 'Picture':
              msg['Text'](msg['FileName']) #下载
              group2_id = group2_id or None
              itchat.send_image(msg['FileName'],group2_id)
              #itchat.send_image(msg['FileName'],group2_id)
          if msg['Type'] == 'Sharing':
              group2_id = group2_id or None
              share_message = "@{}分享\n{} {}".format(msg['ActualNickName'],msg["Url"],msg["Text"])
              itchat.send_msg(share_message,group2_id)
              #print "share"
        if not group1_id:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            group1_instance = itchat.search_chatrooms(name=group1) #本地测试群
            if group1_instance:
                group1_id = group1_instance[0]['UserName']
                itchat.send_msg('发现{}id，信使机器人已激活: )'.format(group1),group1_id)


        if msg['FromUserName'] == group2_id: #针对性处理消息
          if msg["Type"] == 'Text':
            print('微信群{}连接完毕'.format(group2))
            #response = handle_group_msg(msg) # type
            if msg["Text"].startswith('[疑问]') or msg["Text"].startswith('[闭嘴]') or  msg["Text"].startswith('[得意]') or  msg["Text"].startswith('[惊讶]'):
                response = handle_group_msg(msg) # type
                if response['type'] == 'q': # 发送帖子
                    pass # 论坛会触发到两个群
                if response['type'] == 'qa': # 发送帖子
                    to_wechat_msg = response['response']
                    itchat.send_msg(to_wechat_msg,group2_id)

                if response['type'] == 't': #回复帖子
                    to_wechat_msg = '@{} 帖子回复成功 : )'.format(msg['ActualNickName'])
                    itchat.send_msg(to_wechat_msg,group2_id)
                if response['type'] == 'h': #回复帖子
                    to_wechat_msg = response['response']
                    itchat.send_msg(to_wechat_msg,group2_id)
            # 来自群1消息，加入消息队列
            else:
                    group2_msg_list.append(msg)
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logger.info((now,group2,msg['ActualNickName'],msg["Text"]))

          if msg["Type"] == 'Picture':
              msg['Text'](msg['FileName']) #下载
              group1_id = group1_id or None
              itchat.send_image(msg['FileName'],group1_id)
              #itchat.send_image(msg['FileName'],group2_id)
          if msg['Type'] == 'Sharing':
              group1_id = group1_id or None
              share_message = "@{}分享\n{} {}".format(msg['ActualNickName'],msg["Url"],msg["Text"])
              itchat.send_msg(share_message,group1_id)
              #print "share"

        if not group2_id:
            #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
            group2_instance = itchat.search_chatrooms(name=group2) #本地测试群
            if group2_instance:
                group2_id = group2_instance[0]['UserName']
                itchat.send_msg('发现{}id，信使机器人已激活: )'.format(group2),group2_id)
    print("end change_function")




def handle_group_msg(msg):
    # 有多种消息
    logger.info(msg)
    username = msg['ActualNickName'] # 发言者
    content = msg['Text']
    print('handle_group_msg',handle_group_msg)
    '''
    if '/bot/q' in content:
        clean_content = re.split(r'/bot/q', content)[-1]
        response = forum_client.post_thread(username,clean_content)
        return {'type':'q','response':response}

    '''
    if '[疑问]' in content:
        clean_content = re.split(r'\[疑问\]', content)[-1]
        response = forum_client.post_thread(username,clean_content)
        return {'type':'q','response':response}
    if '[惊讶]' in content:
        clean_content = re.split(r'\[惊讶\]', content)[-1]
        answer = qa_bot.howdoi_zh(clean_content.encode('utf-8'))
        response = "@{}\n".format(msg['ActualNickName'])+answer
        return {'type':'qa','response':response}
    #if '/bot/t' in content:
    if content.startswith('[得意]'):
        #判断下正则是够合格
        thread_id,clean_content = re.split(r'\[得意\].*?(?P<id>\d+)', content)[-2:]
        response = forum_client.post_reply(username,thread_id,clean_content)
        return {'type':'t','response':response}

    #if '/bot/h' in content:
    if '[闭嘴]' in content:
        response='Hi @{} 使用说明如下：\n帮助:[闭嘴]\n发帖:[疑问] 帖子内容\n回帖:[得意](id) 回复内容\n搜索:[惊讶] 问题内容'.format(msg['ActualNickName'])
        return {'type':'h','response':response}
    return {'type':None,'response':None}





itchat.auto_login(enableCmdQR=2,hotReload=True) #调整宽度：enableCmdQR=2
#thread.start_new_thread(sync_thread, ())
thread.start_new_thread(itchat.run, ())

while 1:
    change_function()
    time.sleep(1)

