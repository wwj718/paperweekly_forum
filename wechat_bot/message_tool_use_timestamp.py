#!/usr/bin/env python
# encoding: utf-8
from kinto_http import Client # 也可以用requests手动实现
import requests
import time
import json
credentials = ('wwj', 'wwj-test')
server_url = 'http://kinto.just4fun.site/v1' #不能有/
client = Client(server_url= server_url,auth=credentials)
collection = 'forum2wechat_todo' #forum2wechat_todo  # forum2wechat_done
#写到配置文件里
bucket = 'paperweekly'
lastest_thread_timestamp = None # 作为session存储
threads_records_pattern = "/buckets/{bucket}/collections/{collection}/records".format(bucket=bucket,collection=collection)
threads_records_url = "{}{}".format(server_url,threads_records_pattern)
with open("./kinto_cli_cookie.json") as kinto_cli_cookie:
    cookie_data = json.loads(kinto_cli_cookie.read())
    now_timestamp = str(int(time.time()))+"000"
    lastest_thread_timestamp = cookie_data['lastest_thread_timestamp'] if cookie_data['lastest_thread_timestamp'] else now_timestamp #如果为空则从现在开始

def push_thread(thread_id,username,title,content): #使用魔法参数
    data={'thread_id': thread_id, 'username':username,'title':title,'content': content}
    client.create_record(data=data,collection=collection, bucket=bucket)

def get_threads():
    # 获取
    global lastest_thread_timestamp
    if not lastest_thread_timestamp:
        # 到本地查看是否有文件，cookie, dump，挂掉与激活, kinto_cli_cookie.json
        url = threads_records_url
    else:
        url = threads_records_url+"?_since={}".format(lastest_thread_timestamp)
    #records = client.get_records(collection=collection, bucket=bucket)
    # try 直接保护起来
    try:
        response = requests.get(url,auth=credentials)
        print response.json()
        records = response.json()['data']
    except:
        records = []
    # get_records里好像有实现etag,在同义次中应该不会反复请求 ,缓存在哪呢 ,并未缓存
    if records:
        print(records)
        # 找到最大timestamp
        lastest_thread_timestamp = max(record['last_modified'] for record in records)
        with open("./kinto_cli_cookie.json",'w') as kinto_cli_cookie:
            cookie_data = {"lastest_thread_timestamp":lastest_thread_timestamp}
            kinto_cli_cookie.write(json.dumps(cookie_data))
        # 存入cookie，理想状态下，只在程序崩溃才存
        print("len(records):",len(records))
        #client.delete_records(collection=collection,bucket=bucket) #获取即焚
        # 每次不删除而是读取timestamp，获取最大的
        for i in records:
            print(i)
        return records
        #for item in records:
        #    print(item)



#record = client.delete_record(id='8c3b1c8c-ed5b-46d9-a9f0-681f3debb68c',collection=collection, bucket=bucket)


# F10 vim本地运行python代码,或者分屏，在jupyter里做吧
# http://localhost:8888/v1/buckets/default/collections/tasks/records
# http://localhost:8888/v1/buckets/paperweekly/collections/forum2wechat_todo/records 有记录
# kinto-admin本地有问题

if __name__ == '__main__':
    # 只运行一次
    client.create_bucket(bucket)
    client.create_collection(collection, bucket=bucket)

    #  创建记录 数据单元
    #client.create_record(data={'status': 'todo', 'title': 'Todo #2'},
    #                         collection=collection, bucket=bucket)
    # 获取
    '''
    for i in range(3):
        #push_thread('thread_id2','username','title','content')
        get_threads()
        time.sleep(2)
        push_thread('thread_id','username','title','content')
    '''
    #records = client.get_records(collection=collection, bucket=bucket)

    #client.delete_records(collection=collection,bucket=bucket) #获取即焚
    #for item in records:
    #    print(item)
        #这样每次只有新创建的
'''
[{u'username': u'username', u'title': u'title', u'content': u'content', u'thread_id': u'thread_id2', u'last_modified': 1474377043828, u'id': u'd8663a05-e864-4b81-9cf3-99cb03232327'}, {u'username': u'username', u'title': u'title', u'content': u'content', u'thread_id': u'thread_id', u'last_modified': 1474377043820, u'id': u'8f3f7646-9601-4b02-b364-fc8c1b31450d'}]
'''


