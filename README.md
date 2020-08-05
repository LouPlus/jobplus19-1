# jobplus19-1
楼+ Python 实战第 19 期，第 1 组

### 环境配置
* python3.6
* pip安装requirement.txt。命令或许是sudo pip3 install requirement.txt.
* 如果MySQL数据库有密码，记得配置环境变量，若密码为123456： export DEVELOP_DATABASE_URL=mysql://root:123456@localhost:3306/plus_job?charset=utf8
* 迁移数据库，其中，flask db init会创建migrations，若该文件已存在，跳过此行代码。

export FLASK_APP=manage.py  
export FLASK_DEBUG=1  
flask db init  
flask db migrate -m "initial migration"  
flask db upgrade

## 数据生成
1.确保存在jobplus名称的数据库，manage.py同级目录运行 flask db upgrade 生成迁移文件  
2.运行spider_job.py和spider_company.py文件，爬取拉钩网公司信息及51job网职位信息，保存到data_job.json和data_company.json文件 （太频繁，拉钩会弹出登录页）  
3.generate.py文件生成user表、job表、company表测试数据：  

export FLASK_APP=manage.py  
flask shell  
from scripts.generate import run  
run()  

## 启动应用
在虚拟环境中运行startapp.sh启动应用  
应用访问地址：https//127.0.0.1:3333  

## Contributors 

* [助教 - 安西教练](https://github.com/Manchangdx)
* [Clark](https://github.com/Kisslfcr)
* [翠翠](https://github.com/huxinying)
