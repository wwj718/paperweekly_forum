#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import requests

# post thread
# @bot#Q 测试第一个问题
def post_thread(username,content,title="来自paperweekly的问题"):
    headers = {"Authorization": "bearer test", "User-Agent": "wechatClient/0.1 by paperweekly"}
    # 做摘要
    #title = '「来自paperweekly微信群用户@{}」的讨论：{}'.format(username,content)
    # 做摘要 , 摘要
    title = '「来自paperweekly微信群用户@{}」的讨论'(username)
    post_data = {"title": title, "post":content, "category": 3}
    threads_url = 'http://paperweekly.just4fun.site/api/threads/'
    response = requests.post(threads_url, data=post_data,headers=headers,verify=False)
    return response.json()


### 发评论
# @bot#T#2 这是帖子2的答复 正则解析
def post_reply(username,thread_id,content): #用户名 ,用户名就叫paperweekly
    headers = {"Authorization": "bearer test", "User-Agent": "wechatClient/0.1 by paperweekly"}
    content = '「来自paperweekly微信群用户@{}」的回复:{}'.format(username,content)
    post_data = {"post":content} #支持markdown
    threads_url = 'http://paperweekly.just4fun.site/api/threads/{id}/posts/'.format(id=thread_id)
    response = requests.post(threads_url, data=post_data,headers=headers,verify=False)
    return response.json()
