from logging import root
import requests
import json
import time
import pymysql
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
try:
    db=pymysql.connect(host='',user='',password='',database='',charset='gbk')
    cur=db.cursor()
    cur.execute("drop table if exists Comments")
    sqlCre="create table Comments(Name CHAR(20),Time CHAR(30),Comment VARCHAR(400))"
    cur.execute(sqlCre)
    print("新表有了")
except:
    print("快跑，是丁真在测代码")
    print("未抓取评论")
    exit()

print("正在get数据中，因为写了每3秒抓取10条，所以请等待150s以上")

#准备好sql
sqlInsert='INSERT INTO Comments(Name,Time,Comment) VALUE (%s,%s,%s)'

fetch_comment_count = 500
index = 0
page_index = 0
flag = True
pAge=0
with open('comments','w') as fIlestore:
    while flag:
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100019125569&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(page_index)
        page_index += 1
        res = requests.get(url=url, headers=headers)
        text = res.text
        if text=='':
            continue
        pAge+=1
        
        json_str = text.replace('fetchJSON_comment98(', '')[:-2]
        json_obj = json.loads(json_str)
        comments_list = json_obj['comments']
        comments_list_length = len(comments_list)
        time.sleep(random.randint(4,6))
        print(pAge)
        
        for i in range(comments_list_length):
            comments = comments_list[i]['content']
            creation_time = comments_list[i]['creationTime']
            nickname = comments_list[i]['nickname']
            vAlue=(nickname,creation_time,comments)
            # print(vAlue)
            cur.execute(sqlInsert,vAlue)
            index += 1
            if index == fetch_comment_count:
                flag = False
                break
db.commit()
db.close()
# 编码gbk，给的网址给出了具体的编码，不是gb-2312而是gbk
# 因为ip被ban了一段时间，而且有些网页的反爬机制就是什么都不返回，于是乎过滤空白界面
# 另外，写了个随机sleep秒数，不然小心被反爬
# 我们寝室的网络已经被jd顶上了