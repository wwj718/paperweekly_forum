# paperweekly's forum
为[paperweekly](https://zhuanlan.zhihu.com/paperweekly#!)搭建的论坛

# 架构
![](https://raw.githubusercontent.com/wwj718/gif_bed/master/paperweekly_architecture.png)

# 描述
项目由3个组件构成：

*  论坛(forum/bbs)
*  微信机器人（wechat_bot）
*  消息服务

实现paperweekly微信群<==>论坛双向通信（方便问题讨论与归档整理），消息同时可以被多个客户端订阅，目前支持推送到QQ群，目前允许横向拓展到任意消息订阅点（假设不考虑服务器压力）



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
- [ ] 迁移论坛到新的服务器
- [ ] 重新设计user interface，更友好的交互方式, 诸如使用表情:`[疑问]`来激活bot
- [ ] 整合论坛机器人和1，2群转发机器人
- [ ] 撰写教程和开发者文档
- [x] 在markdown中支持数学公式
- [x] 与qq群对接
- [ ] 回复时增加@的功能

### 来自paperweekly群的建议
- [ ] @张俊：帖子内容支持放图片（方便提问）
- [ ] @guangbao: 有帖子的新消息，@发帖人 （ 功能已在开发环境完成，尚未集成）
- [ ] @碱馒头: 精简帖子创建成功的消息，突出id
- [ ] @张源源: 消息内容的组织需要重新排版。群消息和bbs消息要有区分度
- [ ] @侯月源：希望论坛地址变成帖子地址(地址建议采用ip而不是域名，否则体验不好)，能直接跳转近帖子里看历史讨论. 

# 感谢
*  [Misago](https://github.com/rafalp/Misago)
  *  我fork了一个分支，对源码做了调整：[wwj718/Misago](https://github.com/wwj718/Misago/tree/wwj_master)，之后维护这个分支
*  [ItChat](https://github.com/littlecodersh/ItChat)
*  [kinto](https://github.com/Kinto/kinto)
