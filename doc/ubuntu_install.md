# 在ubuntu下部署
网站示例：http://paperweekly.club/

当前论坛部署在ubuntu14.04,其他版本的系统应该也适用

### 系统依赖

```bash
sudo apt-get install libpq-dev python-dev libjpeg-dev libfreetype6-dev
```


### 组件依赖
*  Nginx
*  Gunicorn
*  virtualenv
*  supervisor
*  PostgreSQL
*  redis
*  Misago
*  ItChat
*  Kinto

# 安装论坛
论坛使用[Misago](https://github.com/rafalp/Misago)



### 安装PostgreSQL
建议采用9.5

```bash
# install PostgreSQL 9.5， 早期版本不支持jsonb
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo art-get update 
sudo apt-get install postgresql postgresql-contrib
# sudo su - postgres
# psql
# \password postgres
```

### 配置论坛服务
```bash
#git clone https://github.com/wwj718/Misago  --depth=1 # 我fork了自己的版本(2016.09.18)，之后的定制基于这个版本,--depth=1表示只克隆最新的版本
# 克隆我的分支
git clone https://github.com/wwj718/Misago -b wwj_master
pip install -e ./Misago # -e是edit模式，对源码的修改即时生效 , 源码安装, __version__ = '0.6a1.dev1',
git clone https://github.com/wwj718/paperweekly_forum
pip install -r paperweekly_forum/testforum/requirements.txt
cd paperweekly_forum/testforum
python manage.py migrate
python manage.py createsuperuser
#python manage.py runserver #开发
# 收集静态文件 
python manage.py  collectstatic
gunicorn testforum.wsgi:application --bind 127.0.0.1:8001 -w 4
```


### 配置kinto server（消息服务）
```bash
mkdir ~/kinto_server && cd ~/kinto_server
virtualenv env
source env/bin/activate
pip install kinto
kinto init
kinto migrate
kinto start
```

### 配置nginx
```
sudo apt install nginx
sudo ln -s /home/ubuntu/paperweekly_forum/conf/paper /etc/nginx/sites-enabled/
sudo ln -s /home/ubuntu/paperweekly_forum/conf/kinto_server /etc/nginx/sites-enabled/
sudo service nginx restart
```

###Supervisor
可参考我的这篇文章:[使用Supervisor来管理进程](http://blog.just4fun.site/process-control-system-supervisor.html)



# todo
*  ansible/docker



# 参考
*  [How to thoroughly purge and reinstall postgresql on ubuntu?](：http://stackoverflow.com/questions/2748607/how-to-thoroughly-purge-and-reinstall-postgresql-on-ubuntu)
*  [How to Install PostgreSQL 9.5 on Ubuntu (12.04 - 15.10)](https://www.howtoforge.com/tutorial/how-to-install-postgresql-95-on-ubuntu-12_04-15_10/)
*  [Setting up Django with Nginx, Gunicorn, virtualenv, supervisor and PostgreSQL](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/)

