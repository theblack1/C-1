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
news = {"标题":0,"门类":0,"更新时间":0, "网址":0}
allnews = []
the_order = "哈哈没有设置顺序，耶！！！"
#设定

from urllib import request
from bs4 import BeautifulSoup as bs
import json
import datetime
import os
time = str(datetime.datetime.now())
now = time[0:10] + 'T' +  time[11:20]
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

print("请设置排序方式的数字（'1'为按照标题的utf-8编码输出，\n'2'为按照门类的utf-8编码输出，\n'3'为按照更新时间输出，\n'4'为按照网址输出，\n输入其他数字，则按照原网站的默认顺序输出。\n\n")
print('偷偷备注：我不会按照中文的拼音输出（啊这。。。。。。）')
print('你选择？（请务必填写数字！）')
order = int(input())
if order == 1:
    the_order = "标题"
elif order == 2:
    the_order = "门类"
elif order == 3:
    the_order = "更新时间"
elif order == 4:
    the_order = "网址"
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
    if len(scissors[1]) == 4:
        scissors[1] = '0' + scissors[1]
    update_times.append(scissors[1])
    scissors.clear()
    i = i + 1
#分类完毕

for link3 in soup.find_all('a'):
    links.append(link3['href'])
#获得初略的档案

while n > nub + 1:
    nub = nub + 1  
    news["标题"] = titles[nub]
    news['门类'] = sort_[nub]
    news['更新时间'] = update_times[nub]
    news['网址'] = 'http://www.infzm.com/' + links[nub + 17]
    allnews.append(news.copy())
#获得我们要的的信息


if order:
    allnews = sorted(allnews,key=lambda allnews:allnews[the_order])
#设置排序

article_info = {}
data = json.loads(json.dumps(article_info))
data['被爬网站名称'] = "南方周报'新闻'"
data['排序标准'] = the_order
data['生成时间'] = now
data['这是爬取内容，请过目'] = allnews
article = json.dumps(data,ensure_ascii=False,indent=4,separators=(',', ': '))
#Json内容编写

adress = os.getcwd() + '\\output\\'
if not os.path.exists(adress):
    os.makedirs(adress)

nowcut = now[0:13] + 'h' + now[14:16] + 'm' + now[17:19] + 's'

t = open(adress + nowcut + '.json','w')
t.write(article)
t.close
print('您的文件已输出到工作目录的\"output\"文件夹下，请注意查收。')
#输出！！！
