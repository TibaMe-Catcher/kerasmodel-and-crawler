import requests
from bs4 import BeautifulSoup
import bs4
import os
import time
import random
import pandas as pd

#規劃欄位
columns = ["Title", "Auther", "Joke_url", "Joke"]
total = []
df = pd.DataFrame(columns=columns)

page = 1
for page in range(1,8):
    # 目標網址
    url = 'http://kids.yam.com/joke/topjoke.php?page={}'.format(page)
    # 建立使用者身分    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    res = requests.get(headers = headers, url = url.format(page))
    res.encoding = 'big5'
    html = res.text

    #bs4解析html文件
    soup = BeautifulSoup(html, 'html.parser')
    #定位所在標籤
    topjokes = soup.select("tr[bgcolor = '#ffffff'] ")
    #print(topjokes)

    for each_jokes in topjokes:
        each_title = each_jokes.select('a')
        #print(each_title)
        time.sleep(random.uniform(1,3))

        if len(each_title) == 0:
            pass
        else:
            title = each_title[0].text
            #print(title)
            title_url = 'http://kids.yam.com/joke' + each_jokes.a['href'][1:]
            #print(title_url)

            #爬取標題內容
            each_joke_res = requests.get( url = title_url, headers = headers)
            each_joke_res.encoding = "big5"
            each_joke_soup = BeautifulSoup(each_joke_res.text, 'html.parser')
            each_joke_title = each_joke_soup.select('td[class="boardtitle2"]')[0].text
            each_joke_auther = each_joke_soup.select('div > span[class = "blue"]')[0].text
            each_joke_content = each_joke_soup.select('td[class = "tableword2"]')[0].text.replace('\n','').replace(' ','')

            #print(each_joke_title)
            #print(each_joke_auther)
            #print(title_url)
            #print(each_joke_content)
            time.sleep(random.uniform(2,3))

            #合併欄位
            total = [each_joke_title, each_joke_auther, title_url, each_joke_content]
            df = df.append({"Title":total[0],"Auther":total[1],"Joke_url":total[2],"Joke":total[3]}, ignore_index=True)

page += 1
            
df.to_csv('./jokes.csv',encoding ='utf-8-sig', index= False)