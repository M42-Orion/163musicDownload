#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   音乐下载.py
@Time    :   2020/03/13 15:08:22
@Author  :   刘家委 
@Version :   1.0
@Contact :   2521664384@qq.com
@Desc    :   None
'''

# here put the import lib
import requests
import bs4
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from multiprocessing import Pool


Useragent = UserAgent()
headers = {
    'User-Agent':Useragent.random,
}

def request(url):
    pass
    results = requests.get(url,headers=headers)#get方式请求该网址
    results.encoding = results.apparent_encoding#获取网页编码，对网页内容进行编码，防止乱码产生
    results_json = json.loads(results.text)
    return results_json

def save(i_d,name):
    print(i_d)
    song = request("https://api.imjad.cn/cloudmusic/?type=song&id={}&br=320000".format(i_d))
    response = requests.get(song['data'][0]['url'],headers=headers).content

    # 以二进制的形式写入文件中
    f = open('music\\{}.mp3'.format(name['name']), 'wb')
    f.write(response)
    f.close()
    print(name['name']+"下载完成")

def dowload(track):
    songinf = request("https://api.imjad.cn/cloudmusic/?type=detail&id={}".format(track))#获取每首歌的具体信息
    for name in songinf['songs']:
        try:
            save(track,name)
        except:
            print(name['name']+"为VIP试听音乐，无法下载")

def main(url = "https://api.imjad.cn/cloudmusic/?type=playlist&id=319241983"):
    results_json = request(url)
    pool = Pool()#创建进程池
    pool.map(dowload,[ track['id'] for track in results_json['playlist']['trackIds'] ])
    pool.close() # 将进程池关闭，不再接受新的进程
    pool.join() # 主进程阻塞，只有池中所有进程都完毕了才会通过

if __name__ == "__main__":
    url = input("请输入歌单url:")
    main(url=url)





# API接口
# https://music.163.com/playlist?id=319241983
# https://api.imjad.cn/cloudmusic/?type=detail&id=479944559
# https://api.imjad.cn/cloudmusic/?type=song&id=28012031&br=320000
