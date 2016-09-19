#!/usr/bin/env python
# encoding: utf-8
import redis
import json
r = redis.Redis()

test_json = {}
test_json['foo'] = 'var'

r.publish('test', 'this will reach the listener')
r.publish('test', 'this will reach th listener 2')
r.publish('fail', 'this will not')

r.publish('test', json.dumps(test_json))
# 这部分之后由论坛发送信息到redis,数据结构，json
# http://www.wklken.me/posts/2013/10/19/redis-base.html#2
# HSET
# redis不管数据编码
# Redis has no meaning of "objects", all redis gets are bytes, specifically strings!
# 使用python序列化模块

