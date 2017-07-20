#__author__: xieke
#-*- coding:utf-8 -*-

import requests
from pymongo import MongoClient
from lxml import etree
from time import sleep
import random
#proxies={'http':'http://123.170.255.32:808'}

headers={
'Host': 'www.zhihu.com',
'Connection': 'keep-alive',
'accept': 'application/json, text/plain, */*',
'x-udid': 'AEDCP3Ka1AuPTrUlFFS7QwUJ8TwqOYbI-48=',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
'authorization': 'Bearer 2|1:0|10:1499173548|4:z_c0|92:Mi4wQUJDTXY4SmRLUWtBUU1JX2NwclVDeVlBQUFCZ0FsVk5yQi1EV1FDTTNDWHdOblhoWWF2eUtGXzZwTDRBNDhScEdR|e37134203136d1eb85238e68528fdfa34166b162f77e788cf007dca42a90ce4c',
'Referer': 'https://www.zhihu.com/people/excited-vczh/followers',
'Accept-Encoding': 'gzip, deflate, sdch, br',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
'Cookie': 'd_c0="AEDCP3Ka1AuPTrUlFFS7QwUJ8TwqOYbI-48=|1496026127"; _zap=9eeda231-a294-4833-ba1d-57067b8a3ea9; q_c1=8b086d9971ca4980afc4363a1d5b67b0|1498740913000|1496026126000; _xsrf=c35e7edd2e4fa9669a71165f24a9cc6b; l_cap_id="ZTIyN2Y1ZTZjZDNjNGI3OTg0NmUzMTNiZGVjZWZhNjA=|1499173523|c5143ee6fdde35964ef54a824e66d0f0b5e27c2a"; r_cap_id="YTFiOTA5ODkzNmZkNDA4Y2E2YjQwZjhmZTU4YTI5MTE=|1499173523|4ce29f2e7801bc4da45ab6c15d26a786dc612525"; cap_id="YmJlZTIwYzZlNDcxNDM3Yjk2ZWZlYjdhNGY0ODI5NzM=|1499173523|3afa80ba82f2429de3f8422be45d5a7fab491422"; capsion_ticket="2|1:0|10:1499173543|14:capsion_ticket|44:MzI1ZmE5YjM2NzJkNGVjNjlmNjdhNzM3YjcxMzkxYmE=|f91886be79c5ceb3460a86aac75e2d372b63b114b60bd99afbecfcaf67093836"; z_c0="2|1:0|10:1499173548|4:z_c0|92:Mi4wQUJDTXY4SmRLUWtBUU1JX2NwclVDeVlBQUFCZ0FsVk5yQi1EV1FDTTNDWHdOblhoWWF2eUtGXzZwTDRBNDhScEdR|e37134203136d1eb85238e68528fdfa34166b162f77e788cf007dca42a90ce4c"; aliyungf_tc=AQAAAF0A0kZLIAIAq0uBd5YChX7yRVsj; __utma=51854390.1448698333.1499206763.1499206763.1499206763.1; __utmb=51854390.0.10.1499206763; __utmc=51854390; __utmz=51854390.1499206763.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20151215=1^3=entry_date=20151215=1; _xsrf=c35e7edd2e4fa9669a71165f24a9cc6b'
}

urllist=[]
next_page_url='https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
#获取并解析网页
def get_page(res_url):
    r=requests.get(res_url,headers=headers)
    if r.status_code==200:
        html=etree.HTML(r.text)#用lxml来解析
        print('success in getting page')
        return html
    else:
        print('html error:'+str(r.status_code))
#将数据存入mongodb
def store_to_mongodb(dirc):
    client=MongoClient()
    db=client.zhihu_user_profile
    col=db.user_profile
    col.insert(dirc)
#读取并存入一页的用户链接
def a_page_url(urls):
    global next_page_url
    json = requests.get(urls, headers=headers,timeout=3).json()
    list=json['data']
    for i in list:
        urllist.append(i['url_token'])
    next_page_url=json['paging']['next'] #存储下一页用户的地址

def get_data(url,next_url):
    global next_page_url
    user_data = {}
    tree=get_page(url)#获取到解析后的代码
    user_data['性别']=tree.xpath('//*[@id="root"]/div/main/div/div/meta[2]/@content')
    user_data['昵称']=tree.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]/text()')

    签名=tree.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[2]/text()')
    if 签名:
        user_data['签名'] =签名
    else:
        user_data['签名'] =''

    行业=tree.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/span/div/div[1]/text()[1]')
    if 行业:
        user_data['行业']=行业
    else:
        user_data['行业']=''

    职位=tree.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/span/div/div[1]/text()[2]')
    if 职位:
        user_data['职位']=职位
    else:
        user_data['职位']=''

    学校=tree.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/span/div/div[2]/text()')
    if 学校:
        user_data['学校']=学校
    else:
        user_data['学校']=''

    store_to_mongodb(user_data)#将数据存入mongodb
    a_page_url(next_page_url)
    store_all_users_url()

def store_all_users_url():
    global next_page_url
    j=0
    while next_page_url:
        a_page_url(next_page_url)
        print(j)
        j+=1
        sleep(random.randint(3,6))#休息5秒

def BFS_cpature():#按广度优先搜索爬取
    global next_page_url
    #第一步，以轮子哥为起点，爬取轮子哥的信息并且存储所有关注他的人的url
    url = 'https://www.zhihu.com/people/excited-vczh/followers'
    #@next_page_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
    get_data(url,next_page_url)
    #第二部，重复从urllist中提取url，爬取此人信息并将关注他的人添加到urllist
    i=0
    while urllist[i]:
        url='https://www.zhihu.com/people/{}/followers'.format(urllist[i])
        #next_page_url='https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'.format(urllist[i])
        get_data(url,next_page_url)
        print('获取第',i+1,'条信息')
        i+=1
        sleep(random.randint(3,6))


if __name__=='__main__':
    BFS_cpature()








