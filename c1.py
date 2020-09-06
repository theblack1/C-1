#!/usr/bin/env python3
# -*- coding : utf-8 -*-

n = 0
i = 1
nub = -1
titles = []
kinds = []
update_times = []
sort_ = []
links = []
news = {"Title":0,"Type":0,"Update time":0, "Url":0}
allnews = []
the_order = "I Think U Did Not Set Order!!!!"
#设定

from urllib import request
from bs4 import BeautifulSoup as bs
import json
import datetime
import os
time = datetime.datetime.now()
#引入

requ = request.Request("http://www.infzm.com/topics/t2.html")
requ.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44')
resp = request.urlopen(requ)
doc = resp.read().decode("utf-8")
soup = bs(doc,'html.parser')
[s.extract() for s in soup(class_='pull-right')]
[s.extract() for s in soup('head')]
[s.extract() for s in soup(class_="nfzm-header")]
[s.extract() for s in soup(class_="nfzm-brand")]
#制作一碗汤

while n == 0:
    print ('最多可查询9条,请输入读取条数：')
    n = int(input())
    if n > 9:
        print('你的数字太大了，小一点试试')
        n = 0
    elif n < 0:
        print('你的数字太小了，大一点点嘛~~~')
        n = 0
titles.clear()
#输入读取条数

print("请设置排序方式的数字（'1'为按照标题的utf-8编码输出，\n'2'为按照门类的utf-8编码输出，\n'3'为按照更新时间输出，\n'4'为按照网址输出，\n输入其他数字，则按照原网站的默认顺序输出。\n")
print('偷偷备注：我不会按照中文的拼音输出（啊这。。。。。。）')
print('你选择？（请务必填写数字！）')
order = int(input())
if order == 1:
    the_order = "Title"
elif order == 2:
    the_order = "Type"
elif order == 3:
    the_order = "Update time"
elif order == 4:
    the_order = "Url"
else :
    order = 0
#输入排序标准

for link1 in soup.find_all('h5'):
    title = link1.get_text()
    titles.append(title.lstrip().strip())
titles.pop(0)
#制作标题的list

for link2 in soup.find_all(class_='nfzm-content-item__meta'):
    kind = (link2.get_text()).lstrip().strip()
    kinds.append(kind)
kinds.pop(0)
#获取种类，时间混合列表kinds
#下面开始分类
i = 0

while len(update_times) < 9:
    scissors = kinds[i].split('\n')
    sort_.append(scissors[0])
    update_times.append(scissors[1])
    scissors.clear()
    i = i + 1
i = 0
#分类完毕
now_time = time.strftime("%Y-%m-%dT%H:%M:%S")
for update_time in update_times:
    if update_time.find("分") != -1:
        update_time = update_time.replace('分钟前','')
        update_times[i] = (time + datetime.timedelta(minutes = -int(update_time))).strftime("%Y-%m-%dT%H:%M:%S")
    elif update_time.find("小时") != -1:
        update_time = update_time.replace('小时前','')
        update_times[i] = (time + datetime.timedelta(hours = -int(update_time))).strftime("%Y-%m-%dT%H:%M:%S")
    elif update_time.find("-") != -1:
        update_time = update_time.replace('0','')
        update_times[i] =time.strftime('%Y-') + update_time + time.strftime("T%H:%M:%S")
    i = i + 1
i = 0
#将时间搞定！

for link3 in soup.find_all('a'):
    links.append(link3['href'])
#获得粗略的档案

while n > nub + 1:
    nub = nub + 1  
    news["Title"] = titles[nub]
    news['Type'] = sort_[nub]
    news['Update time'] = update_times[nub]
    news['Url'] = 'http://www.infzm.com/' + links[nub + 17]
    allnews.append(news.copy())
#获得我们要的的信息


if order:
    allnews = sorted(allnews,key=lambda allnews:allnews[the_order])
#设置排序

article_info = {}
data = json.loads(json.dumps(article_info))
data['Name'] = "南方周报'新闻'"
data['Order'] = the_order
data['Generate at'] = now_time
data['Date'] = allnews
article = json.dumps(data,ensure_ascii=False,indent=4,separators=(',', ': '))
#Json内容编写

adress = os.getcwd() + '\\output\\'
if not os.path.exists(adress):
    os.makedirs(adress)

creat_time = (time).strftime("%Y-%m-%d-%H-%M-%S")

t = open(adress + creat_time + '.json','w',encoding = 'utf-8')
t.write(article)
t.close
print('您的文件已输出到' + adress + '文件夹下，请注意查收。')
#输出！！！
