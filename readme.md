# paperweekly's forum
为[paperweekly](https://zhuanlan.zhihu.com/paperweekly#!)构建的论坛

ps：群里进行头脑风暴，需求确定得很快，用了一晚大概实现了骨架，源码粗糙，见笑，欢迎改进 : )

# 描述
项目由3个组件构成：

*  论坛(forum/bbs)
*  微信机器人（wechat_bot）
*  消息服务

实现paperweekly微信群<==>论坛双向通信（方便问题讨论与归档整理），消息同时可以被多个client订阅，支持推送到QQ群，允许被任意多得消息订阅点订阅（假设不考虑服务器压力）

# 场景
当大家在微信群中交流时，消息可以被推送到论坛中以便归档。当论坛有新的讨论时，将自动推送到微信群，大家可以据此展开讨论，并将讨论结果推往论坛以解答问题。

设想这种场景：进行头脑风暴时，大家在微信群中漫谈、碰撞、擦出火花，任何成员看到亮点即可使用:`/bot/q xxx`将点子推往论坛做记录，观点争论问题也是如此。

当群成员看到来自论坛的问题，使用:`/bot/t/(id) xxx`即可对问题及时作出回答，论坛那头在线急等的小伙伴便可看到

同时更多的微信群和QQ群可以订阅讨论的结果，华山论剑，天下观之

# 架构
![](https://raw.githubusercontent.com/wwj718/gif_bed/master/paperweekly_architecture.png)

# 测试站点
http://paperweekly.just4fun.site/

![](https://raw.githubusercontent.com/wwj718/gif_bed/master/paperweekly_all.jpg)


# 依赖
*  Nginx
*  Gunicorn
*  virtualenv
*  supervisor 
*  PostgreSQL 
*  redis
*  Misago
*  ItChat
*  Kinto

# todo
- [x] 在服务器部署论坛: paperweekly.just4fun.site
- [x] 微信发送帖子到论坛
- [x] 论坛发送帖子到微信群
- [x] bot的交互界面(help:/bot/h,question:/bot/q,thread reply:/bot/t/(id))
- [x] 迁移论坛到新的服务器
- [ ] 重新设计user interface，更友好的交互方式, 诸如使用表情:`[疑问]`来激活bot
- [x] 整合论坛机器人和1，2群转发机器人（我这里基于itchat实现了一个，@碱馒头兄也有一个版本，我比较偏好itchat就自己实现了）
- [ ] 撰写教程和开发者文档
- [x] 在markdown中支持数学公式
- [x] 与qq群对接
- [x] 回复时增加@的功能
- [x] 从stackoverflow搜索最佳答案
- [x]  支持转发图片和sharing格式信息

### 来自paperweekly群的建议
- [x] @张俊：帖子内容支持放图片（方便提问）
- [ ] @guangbao: 有帖子的新消息，@发帖人 （ 功能已在开发环境完成，尚未集成）
- [ ] @碱馒头: 精简帖子创建成功的消息，突出id
- [ ] @张源源: 消息内容的组织需要重新排版。群消息和bbs消息要有区分度
- [ ] @侯月源：希望论坛地址变成帖子地址(地址建议采用ip而不是域名，否则体验不好)，能直接跳转近帖子里看历史讨论. 

# 感谢
*  [Misago](https://github.com/rafalp/Misago)
  *  我fork了一个分支，对源码做了调整：[wwj718/Misago](https://github.com/wwj718/Misago/tree/wwj_master)，之后维护这个分支
*  [ItChat](https://github.com/littlecodersh/ItChat)
*  [kinto](https://github.com/Kinto/kinto)
