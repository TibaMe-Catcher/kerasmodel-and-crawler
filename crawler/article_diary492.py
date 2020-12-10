#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import json
from lxml import etree
import time


# In[5]:


#目標網址
url = 'https://kuratica.pixnet.net/blog/category/1423591/{}'
    
#建立使用者身分
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

res = requests.get( url = url , headers = headers )
res.encoding = 'utf-8'

#取所有頁數(共25頁)
#n=25
#for i in range(0,n):

html = res.text
#bs4解析html文件
soup = BeautifulSoup(html, 'html.parser')


# In[132]:


#定位資料所在標籤
diaries = soup.select('div[class = "article"]')

for each_diary in diaries:
    
    each_diary_title = each_diary.a.text
    each_diary_url = each_diary.a['href']

    
    each_diary_res = requests.get( each_diary_url , headers = headers )
    each_diary_res.encoding = 'utf-8'
    each_diary_soup = BeautifulSoup(each_diary_res.text, 'html.parser')
    
    each_diary_content = each_diary_soup.select('div[class = "article-content-inner"]')[0].text
    
    print("============")
    print(each_diary_title)
    print(each_diary_url)
    print("==")
    print(each_diary_content)



# # 正式爬取
# 爬全部頁數(換頁)+存檔

# In[145]:


import requests
from bs4 import BeautifulSoup
import os
import time
import random
#import pandas as pd
#import json
#from lxml import etree


#resource_path = r'./Diary'
#if not os.path.exists(resource_path):
#    os.mkdir(resource_path)

#目標網址
url = 'https://kuratica.pixnet.net/blog/category/1423591/{}'
page = 1

#建立使用者身分
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

#取所有頁數(共25頁)
n=25
for i in range(0,n):

    res = requests.get( url = url.format(page) , headers = headers )
    res.encoding = 'utf-8'
    html = res.text
    time.sleep(random.uniform(1,3))

    #bs4解析html文件
    soup = BeautifulSoup(html, 'html.parser')

    #定位資料所在標籤
    diaries = soup.select('div[class = "article"]')
    
    #取個別文章內容
    for each_diary in diaries:
        each_diary_title = each_diary.a.text
        each_diary_url = each_diary.a['href']
        
        each_diary_res = requests.get( each_diary_url , headers = headers )
        each_diary_res.encoding = 'utf-8'
        each_diary_soup = BeautifulSoup(each_diary_res.text, 'html.parser')
        each_diary_content = each_diary_soup.select('div[class = "article-content-inner"]')[0].text
        
        print("============")
        print(each_diary_title)
        print(each_diary_url)
#        print("==")
#        print(each_diary_content)
    
    #存檔
        try:
            with open("./Diary/{}.txt".format(each_diary_title),"w",encoding="utf-8") as f:
                f.write(each_diary_content)
        except FileNotFoundError:
            with open("./Diary/{}.txt".format(each_diary_title.replace("/", "").replace("?","").replace("<","").replace(">","").replace("|","").replace("*","")),"w",encoding="utf-8") as f:
                f.write(each_diary_content)
        except OSError:
            pass

    #換頁
    page += 1
    url = 'https://kuratica.pixnet.net/blog/category/1423591/{}'.format(page )
        


# In[ ]:




