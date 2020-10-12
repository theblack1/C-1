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
set_ = 0
#topic = 2
#设定

from urllib import request
from bs4 import BeautifulSoup as bs
import json
import datetime
import os
import sys
time = datetime.datetime.now()
#引入
'''
print ("输入数字，选择您要摘取的模块")
print ("0，首页\n1，推荐\n2,新闻\n3,观点\n4，文化\n7，人物\n8,影像\n6，专题，\5生活\n131，视频（只能查看标题）")
topic = int(input())
#选择要查询的板块
'''
while len(titles) == 0:
    requ = request.Request("http://www.infzm.com/topics/t2.html")
    requ.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44')
    resp = request.urlopen(requ)
    doc = resp.read().decode("utf-8")
    soup = bs(doc,'html.parser')
    [s.extract() for s in soup(class_='pull-right')]
    [s.extract() for s in soup('head')]
    [s.extract() for s in soup(class_="nfzm-header")]
    [s.extract() for s in soup(class_="nfzm-brand")]
#print(soup.get_text)
#制作一碗汤
    for link1 in soup.find_all(class_='nfzm-content-item__title'):
        title = link1.get_text()
        titles.append(title.lstrip().strip())

    
#制作标题的list

'''
if len(titles) == 0:
    print('不好意思，你这里用不了，\n（我确认我的电脑可以允许这个程序！！！）\n这是历史遗留问题，我会回来解决的！但是不是现在。')
    print("输入任意数字确认退出")
    n = int(input())
    sys.exit()
'''

titles.pop(0)

max_ = len(titles)
while n == 0:
    print ('最多可查询' ,max_ , '条,请输入读取条数：')
    n = int(input())
    if n != 416:
        if n > max_:
            print('你的数字太大了，小一点试试')
            n = 0
        elif n <= 0:
            print('你的数字太小了，大一点点嘛~~~')
            n = 0
    else:
        set_ = 1
        print("Test modle on")
        n = max_
#输入读取条数

if set_ == 0 :
    print("\n请设置排序方式:\n'1'为按照标题的utf-8编码输出，\n'2'为按照门类的utf-8编码输出，\n'3'为按照更新时间输出，\n'4'为按照网址输出，\n输入其他数字，则按照原网站的默认顺序输出。\n")
    print('请输入：')
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
else:
    order = 0
#输入排序标准


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
