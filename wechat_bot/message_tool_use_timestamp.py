#!/usr/bin/env python
# encoding: utf-8
from kinto_http import Client # 也可以用requests手动实现
credentials = ('wwj', 'wwj-test')
server_url = 'http://paperweekly.just4fun.site:8888/v1'
client = Client(server_url= server_url,auth=credentials)
collection = 'forum2wechat_todo' #forum2wechat_todo  # forum2wechat_done
#写到配置文件里
bucket = 'paperweekly'


def push_thread(thread_id,username,title,content): #使用魔法参数
    data={'thread_id': thread_id, 'username':username,'title':title,'content': content}
    client.create_record(data=data,collection=collection, bucket=bucket)

def get_threads():
    # 获取
    records = client.get_records(collection=collection, bucket=bucket)
    if records:
        #client.delete_records(collection=collection,bucket=bucket) #获取即焚
        print(records)
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
    push_thread('thread_id','username','title','content')
    push_thread('thread_id2','username','title','content')
    get_threads()
    #records = client.get_records(collection=collection, bucket=bucket)

    #client.delete_records(collection=collection,bucket=bucket) #获取即焚
    #for item in records:
    #    print(item)
        #这样每次只有新创建的
'''
[{u'username': u'username', u'title': u'title', u'content': u'content', u'thread_id': u'thread_id2', u'last_modified': 1474377043828, u'id': u'd8663a05-e864-4b81-9cf3-99cb03232327'}, {u'username': u'username', u'title': u'title', u'content': u'content', u'thread_id': u'thread_id', u'last_modified': 1474377043820, u'id': u'8f3f7646-9601-4b02-b364-fc8c1b31450d'}]
'''


