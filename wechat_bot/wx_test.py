#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from wxbot import *
import requests

def post2forum(content,title="来自paperweekly的问题"):
    headers = {"Authorization": "bearer test", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    post_data = {"title": title, "post":content, "category": 3}
    threads_url = 'http://127.0.0.1:8000/api/threads/'
    response = requests.post(threads_url, data=post_data,headers=headers,verify=False)
    print(response.json())

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        #if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print(msg["content"]["data"])
            if "Question" in msg["content"]["data"]:
                print('[Question]')
                content = msg["content"]["data"]
                post2forum(content)
            # self.send_msg_by_uid(u'hi', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png' # tty linux
    bot.run()


if __name__ == '__main__':
    main()
