# kinto client
将[kinto](https://github.com/Kinto/kinto)用作消息队列（这里使用消息队列的广义意思，概念上就是存储字符串的一个队列）

# Why
### 为何需要消息队列
我想把wechat bot和forum分布在不同机器上，两边需要通信，决定采用传递消息的方式来通信。消息存储在一个队列里（消息是事件的载体）

### 为何不是redis活着RabbitMQ
我想把wechat bot和forum分布在不同机器上，forum跑在云服务器上，wechat bot跑在我的树莓派里（因为是私人微信，放在本地树莓派里比较有安全感），由此一来它们是分布式的系统。

redis的subpub可以轻松解决我的需求，实际上我已经实现了基于redis的通信机制，但redis的远程访问，设计很多安全问题，忍痛弃用

RabbitMQ比较重，需求很轻量，不想引入额外复杂度

### 为何选择kinto
为何选择kinto用python构建，我喜欢python : ) , 此外kinto小而美，所以没采用firebase或是parse

关于kinto可以参考我的这篇文章:[如何架空经常500的后端程序员](http://blog.just4fun.site/kinto-note-05-31.html)

在这个需求中，kinto作为一个python库，运行起来，消息直接存在内存汇总即可（后期有需要存入postgres数据库）, 小而美 :)

# 依赖
使用Kinto的python客户端:[kinto-http](https://github.com/Kinto/kinto-http.py)

# 消息存取流程
*  `微信->论坛` 的消息通信机制已经完成，这部分不需要外部消息队列
*  kinto主要服务于`论坛->微信`的消息存取,下边描述

论坛发生变更（目前主要关注帖子/评论的创建），把消息发送到kinto server上，kinto server是一个JSON storage service


# 消息监控
可以直接使用[kinto-admin](https://kinto.github.io/kinto-admin/)

可以把这个网页视为你的client，填入你的server和凭证即可,官方的管理端需要https，无法对接本地http服务

# todo
如果kinto-http之后实现了synchronisation机制，利用了客户端缓存，我们就不需要删除record了，每次查询都将获得新的信息（类似pubsub），原理上是通过时间戳完成

细节参考:[Synchronisation](http://kinto.readthedocs.io/en/stable/tutorials/synchronisation.html#sync-implementations)

# 客户端工具
wechat_bot/message_tool.py

