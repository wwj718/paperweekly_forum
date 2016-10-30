# mac下开发
我自己在mac下开发，记录开发的环境搭建以及笔记


# 安装论坛
官方推荐真是使用使用0.5版，0.6版还在开发中，不稳定，新版有许多吸引人的特性，我看了源码和项目的架构，觉得hold得住，自己fork个版本来继续开发也没啥问题，于是决心，吃新鲜螃蟹.

项目文档不大完备，安装起来比较折腾,如果你熟悉django，就没啥问题,工程化方面做得不好（开发者少）

如果你按照官方文档安装，可能会遇到一些坑。我把我遇到的坑列出

Misago0.6版目前只支持PostgreSQL。我们先安装数据库

## 论坛选型
群里熟悉python的小伙伴居多，选型上放弃了discourse。一番筛选下来，决定使用[Misago](https://github.com/rafalp/Misago)

>  Misago is fully featured forum application written in Python and ES6, powered by Django and React.js

#### 介绍
我们引用该项目首页的介绍：

>  Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

该项目主要由波兰程序员[Rafał Pitoń](https://github.com/rafalp)推进，他完成了绝大多数的代码实现

技术栈很新,用的多是当下正流行的开源组件,折腾起来很有意思.

#### 特性
就论坛应用而言，这个项目的设计很现代

*  基于web的管理界面（和discourse类似）: `/admincp/`   

![](http://oav6fgfj1.bkt.clouddn.com/paperweekly862d225b.png)

*  对markdown的支持
*  todo
    *  学霸多。支持数学公式



### 项目依赖
##### PostgreSQL数据库
这是个强依赖，无法替换为其他数据库。PostgreSQL是个十分优秀的开源数据库

我们先配置好数据库环境，如果你对PostgreSQL不熟悉,可以先阅读:[PostgreSQL新手入门](http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)

##### 安装数据库
```bash
brew cask install postgres # 装好后是postgres.app ，是9.5 , 有图形界面
brew  install postgres
# sudo pip install psycopg2
```

数据库跑起来后，使用`psql`进入数据库,接下来创建用户和数据库并分配好权限

```
:::text
\password wwj  # 我的当前用户是wwj,为当前用户用户设置一个密码
CREATE USER dbuser WITH PASSWORD 'password';  # 创建数据库用户dbuser（刚才的是系统用户），并设置密码
CREATE DATABASE exampledb OWNER dbuser; # 创建用户数据库，这里为exampledb，并指定所有者为dbuser
GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser; # 将exampledb数据库的所有权限都赋予dbuser
\q # 退出控制台（也可以直接按ctrl+D）
```

[PostgreSQL新手入门](http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)一问中给出了其他方法，大家你可以参考

在mac下postgres的服务端使用postgres.app,比较好控制。至于为何还要用`brew install postgres`,主要是为了满足python客户端依赖

#### postgres笔记
登录数据库：`psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432`

另外推荐一个很受欢迎的命令行工具:[pgcli](https://github.com/dbcli/pgcli),使用pgcli连接数据库:`pgcli -U dbuser -d exampledb -h 127.0.0.1 -p 5432`

还有个工具:[sandman2](https://github.com/jeffknupp/sandman2),用于提供数据库的rest接口,方面我们直接侵入拓展，暴力美学

sandman2ctl postgresql+psycopg2://dbuser:wwjtest@localhost/exampledb. 访问：`http://127.0.0.1:5000/admin/`


### 论坛配置文件
forum项目中，数据库相关的设置如下:

```
DATABASES = {
      'default': {
          # Only PostgreSQL is supported
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'exampledb',
          'USER': 'dbuser',
          'HOST': 'localhost',
          'PASSWORD': 'password',
          'PORT': 5432,
      }
}
```

### 安装论坛
推荐方法二

#### 方法一
安装官方的做法，应该这样:

```bash
git clone https://github.com/rafalp/Misago
cd Misago
# 使用virtualenv建立虚拟环境
python setup.py install
pip install -r misago/project_template/requirements.txt
misago-start.py testforum # 项目本身有坑，你可以直接使用我建立好的论坛: https://github.com/wwj718/paperweekly_forum
# 构建项目依赖
cd testforum
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

在此解释下Misago个testforum的关系，这就类似于，django和django site的关系，testforum可以看做Misago的示例，Misago里是作者写好的论坛的核心部件，使用misago-start.py新建的工程，将直接使用Misago的部件来够构建论坛，这样的好处是，用的定制化内容可以放在自建项目里，而核心组件由社区推动，这是开源社区常见做法



#### 方法二
我已经把项目剥离到github，如果你安装我的版本，坑可能少些

```
# 使用virtualenv建立虚拟环境
# 先把pip升级到1.8以上: pip install --upgrade pip

git clone https://github.com/wwj718/Misago  --depth=1 # 我fork了自己的版本(2016.09.18)，之后的定制基于这个版本,--depth=1表示只克隆最新的版本
pip install -e ./Misago # -e是edit模式，对源码的修改即时生效 , 源码安装, __version__ = '0.6a1.dev1',
git clone https://github.com/wwj718/paperweekly_forum
pip install -r paperweekly_forum/testforum/requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

##### 我的调整
*  使用OAuth2Authentication(django-oauth-toolkit)，引出restful接口与外部bot通信
*  开启/admin
*  支持跨域请求

默认的设置:[conf/defaults](https://github.com/rafalp/Misago/blob/master/misago/conf/defaults.py)，这是django层面的默认设置，可以在forum项目的settings.py中自行覆盖


# 跑起来试试
测试工具分别使用[httpie](https://github.com/jkbrzt/httpie)和[requests]()，当然你也可以使用postman或者curl

测试网站为`paperweekly.just4fun.site` (目前论坛已经迁往 paperweekly.club)

#### 发帖
`http post  http://paperweekly.just4fun.site/api/threads/ title='from httpie' category=3  post="from httpie"  "Authorization: Bearer xxx" ` 返回：

```json
{
    "id": 2,
    "title": "from httpie",
    "url": "/thread/from-httpie-2/"
}
```

下边用[requests](https://github.com/kennethreitz/requests)测试

```
def post2forum(content,title="来自paperweekly的问题"):
    threads_url = "http://paperweekly.just4fun.site/api/threads/"
    headers = {"Authorization": "bearer test", "User-Agent": "wechatClient/0.1 by paperweekly"}
    post_data = {"title": title, "post":content, "category": 3}
    response = requests.post(threads_url, data=post_data,headers=headers,verify=False)
    return response.json() #json
print post2forum("from requests")
```

### 发评论
`http post http://paperweekly.just4fun.site/api/threads/2/posts/ post='test2'  "Authorization: Bearer test"`  



### 论坛管理
*  /admincp/：管理界面入口(需要管理员权限) 
*  /admincp/settings/basic/ :  论坛基本设置，名称等
*  /admincp/settings/users/ : 注册机制设置




# 与微信通信
我们使用[wxBot](https://github.com/liuwons/wxBot)来与微信通信，视为微信的io即可

为了在linux命令行中使用，需要设置 WXBot 对象的 conf['qr'] 为 tty ,如此一来二维码直接在终端打印出

出现1102错误，之后换用:[ItChat](https://github.com/littlecodersh/ItChat)


### 将微信群中的问题类消息发往论坛
源码参考:[wx_test.py](https://github.com/wwj718/paperweekly_forum/blob/master/wx_test.py)


# 开发笔记

### 顶部警告
'Warning: This is unreleased version of Misago. There's no support or update path available for it!'

Misago中misago/templates/misago/base.html 


### smtplib 配置

```
# smtp
#EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com' #使用qq邮箱
EMAIL_HOST_PASSWORD = 'xx' #my gmail password
EMAIL_HOST_USER = 'xx@qq.com' #my gmail username
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```


### postgres备份
```
pg_dump exampledb > /tmp/exampledb.sql
#恢复
psql  exampledb <  /tmp/exampledb.sql
```

### 数据迁移
```
pg_dump -d exampledb -U dbuser -W -h 127.0.0.1 -p 5432 > /tmp/exampledb.sql 
scp  /tmp/exampledb.sql wwj@139.162.234.107:/tmp
sudo su - postgres
psql  exampledb <  /tmp/exampledb.sql #先删除原有数据
# 备份到git里，大文件
pg_dump -Fc -d exampledb  -U dbuser -W -h 127.0.0.1 -p 5432 > /tmp/exampledb.bak # compressed binary format 
```

### 论坛翻译

```
django-admin makemessages -l zh_CN
django-admin compilemessages
```

### 中文翻译（年代久远）
https://github.com/fooying/misago-trans-cn


### 论坛markdown部分
*  bleach ： Bleach is a whitelist-based HTML sanitizing library that escapes or strips markup and attributes.  漂白剂这个名字很贴切
*  [markdown](https://github.com/waylan/Python-Markdown)==2.6.6
      *  [文档](https://pythonhosted.org/Markdown/)
*  mathjax: 直接在前端解析多好（纯js）


# 论坛发送消息（视为webhook output)
https://github.com/rafalp/Misago/blob/master/misago/threads/api/threads.py#L90



# 参考
*  [postgres Backup and Restore](http://postgresguide.com/utilities/backup-restore.html)
