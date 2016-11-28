#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import threading
import time
import random
import re
import datetime
import thread
#import tinydb
from localuser import LocalUserTool

'''
#  重构
*  3个小组
*  先完成转发部分
*  采用心想事成法（sicp）
    *  send_message 假设存在，发给其他两个群
    *  两个群订阅即可，类中有on emit方法(on 方法是并行)
    *  消息本身有身份，如果合适就listen on
*  基于事件驱动/多线程
    *  Queue/blinker 线程安全
'''

# itchat for wechat
import itchat  # 另一个微信库：https://github.com/littlecodersh/ItChat
from itchat.content import TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO, SHARING # RECORDING 语音

#########
#log
import logging
LOG_FILE = "/tmp/wechat_3group.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#########


#class GroupBot(threading.Thread): # 作为threading类
class GroupBot(object):  # 没必要多线程
    """Docstring for GroupBot. """

    def __init__(self, group_name):
        """TODO: to be defined1.

        :group_name: TODO

        """
        #threading.Thread.__init__(self)
        self._group_name = group_name
        self._group_id = None

    def __str__(self):
        return self._group_name
    def set_id(self,group_id):
        self._group_id = group_id


    def __repr__(self):
        return self._group_name
    #@itchat.msg_register([TEXT,SHARING,PICTURE], isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        print("reply message!")  # 消息接受在主进程中接受一次即可,没必要多线程,需要一个只能的send_message

    def run(self):
        wait_time = random.randrange(1, 3)
        print("thread {}(group_name:{}) will wait {}s".format(
            self.name, self._group_name, wait_time))  # 默认的名字:Thread-1
        time.sleep(wait_time)
        print("thread {} finished".format(self.name))


def forward_message(msg,src_group,target_groups):
    '''按类型发消息'''
    if msg["Type"] == 'Text':
        '''
        print(itchat.get_friends())
        # 消息入口
        logger.debug(msg)
        username = msg["ActualUserName"] # 发言用户id 群id:FromUserName
        user = itchat.search_friends(userName=username)
        '''
        logger.debug(msg) # log
        # 跨群@ , 至于私聊 可以截图发微信号
        #把用户都存下,多给msg一个属性 at_id
        actual_user_name = msg["ActualNickName"]
        localuser_tool = LocalUserTool()
        at_id = localuser_tool.get_at_id(actual_user_name)
        if not at_id:
            at_id = localuser_tool.set_at_id(actual_user_name)
        # 改造消息属性，使其多一个at_id
        msg["at_id"] = at_id
        match_at_message = re.match(r'at *(?P<message_at_id>\d+) *(?P<message_text>.*)', msg["Text"])



        '''
        if 1==2:#msg["Text"].startswith('[疑问]') or msg["Text"].startswith('[闭嘴]') or msg["Text"].startswith('[得意]') or msg["Text"].startswith('[惊讶]'):
            # 这些是系统功能不转发
            #response = handle_text_msg(msg)  # type
            response = {'type':None,'response':None}
            if response['type'] == 'q':  # 发送帖子
                pass  # 论坛会触发到两个群
            if response['type'] == 'qa':  # 发送帖子
                to_wechat_msg = response['response']
                itchat.send_msg(to_wechat_msg,src_group)

            if response['type'] == 't':  #回复帖子
                to_wechat_msg = '@{} 帖子回复成功 : )'.format(msg['ActualNickName'])
                itchat.send_msg(to_wechat_msg,src_group)
            if response['type'] == 'h':  #回复帖子
                to_wechat_msg = response['response']
                itchat.send_msg(to_wechat_msg,src_group)
        # 写一个跨群at，先检测消息 at 1 你好
        '''
        if match_at_message:
            groupdict = match_at_message.groupdict()
            message_at_id = groupdict.get("message_at_id")
            message_text = groupdict.get("message_text")
            actual_user_name = localuser_tool.get_actual_user_name(int(message_at_id))

            for group in target_groups:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logger.info((now, group._group_name, msg['ActualNickName'], msg["Text"]))
                message = u'@{} \n{}-at_id:{} 发言 ：\n{}'.format(actual_user_name,msg['ActualNickName'],msg['at_id'],message_text)
                #message = u'@{}\u2005\n : {}'.format(actual_user_name,message_text)
                itchat.send(message,group._group_id)
        else:
            #普通文本消息
            for group in target_groups:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logger.info((now, group._group_name, msg['ActualNickName'], msg["Text"]))
                #if group._group_id:
                message = '{}-at_id:{} 发言 ：\n{}'.format(msg['ActualNickName'],msg['at_id'],msg['Text'])
                itchat.send(message,group._group_id)
    if msg["Type"] == 'Picture':
            msg['Text'](msg['FileName'])  #下载
            for group in target_groups:
                itchat.send_image(msg['FileName'], group._group_id)
    if msg['Type'] == 'Sharing':
        share_message = "@{}分享\n{} {}".format(
            msg['ActualNickName'], msg["Url"].replace("amp;", ""), msg["Text"])
        for group in target_groups:
            itchat.send_msg(share_message, group._group_id)


def get_target_groups(src_group, groups):
    '''
    src_group 是 对象
    groups: 所有的微信组，全集
    '''
    list_groups = list(groups)
    list_groups.remove(src_group)  # target groups
    return list_groups
    #print("from {} to {}".format(src_group._group_name,",".join([group._group_name for group in list_groups])))

def handle_text_msg(msg):
    #username = msg['ActualNickName'] # 发言者
    content = msg['Text']

    if '[疑问]' in content:
        clean_content = re.split(r'\[疑问\]', content)[-1]
        response = "response"#forum_client.post_thread(username,clean_content)
        return {'type':'q','response':response}
    if '[惊讶]' in content:
        clean_content = re.split(r'\[惊讶\]', content)[-1]
        answer = "qabot"#qa_bot.howdoi_zh(clean_content.encode('utf-8'))
        response = "@{}\n".format(msg['ActualNickName'])+answer
        return {'type':'qa','response':response}
    #if '/bot/t' in content:
    if content.startswith('[得意]'):
        #判断下正则是够合格
        thread_id,clean_content = re.split(r'\[得意\].*?(?P<id>\d+)', content)[-2:]
        response = "response"#forum_client.post_reply(username,thread_id,clean_content)
        return {'type':'t','response':response}

    #if '/bot/h' in content:
    if '[闭嘴]' in content:
        response='Hi @{} 使用说明如下：\n帮助:[闭嘴]\n发帖:[疑问] 帖子内容\n回帖:[得意](id) 回复内容\n搜索:[惊讶] 问题内容'.format(msg['ActualNickName'])
        return {'type':'h','response':response}
    return {'type':None,'response':None}




# 全局设置
group1_name = 'paper测试1'
group2_name = 'paper测试2'
group3_name = '测试m'
#group1_name = 'PaperWeekly交流群'
#group2_name = 'PaperWeekly交流二群'
#group3_name = 'PaperWeekly交流三群'
#print "Start main threading"
group1 = GroupBot(group_name=group1_name)
group2 = GroupBot(group_name=group2_name)
group3 = GroupBot(group_name=group3_name)
groups = (group1, group2, group3)  #list原有结构会被改变 ,内部元素是够会不可变



def main():
    #group1_name = 'PaperWeekly交流群'
    #group2_name = 'PaperWeekly交流二群'
    #group3_name = 'PaperWeekly交流三群'
    #forward_message("test", group1, groups)

    @itchat.msg_register([TEXT,SHARING,PICTURE], isGroupChat=True)  # 群聊，TEXT ， 可视为已经完成的filter
    def simple_reply(msg):
        #设置为nolocal
        global groups
        print("simple_reply begin msg")
        for group in groups:
            if msg['FromUserName'] == group._group_id:
                src_group = group
                target_groups = get_target_groups(src_group, tuple(groups))
                # 筛选出已激活的
                active_target_groups = [group for group in target_groups if group._group_id]
                forward_message(msg,src_group,active_target_groups)
            if not group._group_id:
                print(group._group_id) #None
                # 不存在的时候
                #如果找到群id就不找，否则每条消息来都找一下,维护一个群列表,全局
                group_instance = itchat.search_chatrooms(name=group._group_name
                                                         )  #本地测试群
                if group_instance:
                    group.set_id(group_instance[0]['UserName']) #没有设置成功？
                    print("{}激活,group_id:{}".format(group._group_name,group._group_id))
                    itchat.send_msg('机器人已激活: )', group._group_id)

    print "End Main function"

itchat.auto_login(enableCmdQR=2,hotReload=True) #调整宽度：enableCmdQR=2
#thread.start_new_thread(sync_thread, ())
thread.start_new_thread(itchat.run, ())

while 1:
    main()
    time.sleep(1)

