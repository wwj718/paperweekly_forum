#!/usr/bin/env python
# encoding: utf-8
import redis
#import wdb  #本地调试比ipdb方便
r = redis.Redis()
pubsub = r.pubsub()
channels = ['test']
pubsub.subscribe(channels)
messages = pubsub.get_message()
# 发布的时候必须在线？
# 客户端先在线 然后等待发布,客户端先等待
# 订阅者要先在线

#ipdb.set_trace()
#wdb.set_trace()
messages #每次只取一条，消息是序列化后的, json
# {'pattern': None, 'type': 'message', 'channel': 'test', 'data': '{"foo": "var"}'}
