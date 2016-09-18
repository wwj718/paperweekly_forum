#!/usr/bin/env python
# encoding: utf-8
import redis
r = redis.Redis()

r.publish('test', 'this will reach the listener')
r.publish('test', 'this will reach th listener 2')
r.publish('fail', 'this will not')

r.publish('test', 'KILL')
