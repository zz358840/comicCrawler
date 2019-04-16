# 指定python執行路徑 這個code不需要使用這行 要也可以 看個人需求               !/Users/zz358840/python3/anaconda3/bin/python
# -*- coding: utf-8 -*-
# selenium是一個可依附在瀏覽器執行的強大套件
from selenium import webdriver
# bs4是整理html原始碼好用的工具 也有搜尋功能
from bs4 import BeautifulSoup
# http相關操作必須載入的重要套件
import requests
# 牽涉到系統層級操作需要引入的套件
import os

# 漫畫官網
# http://www.comicbus.com/
# 要先找到要爬的漫畫的第一頁 章節與頁數去掉如下方範例

# 要爬的網址
url='http://v.nowcomic.com/online/manga_7257.html?ch='
# 章節
ch=4
# 目前頁數
page=None
# 這個章節的總頁數
pagenum=None
# 漫畫真正所在位置網址
newurl=''
# 可以指定firefox chrome 我使用的這個是背景執行的模擬瀏覽器 不會有GUI的畫面跳出 不過在某些情況會無法使用 會被判定瀏覽器太舊 原因不明
driver = webdriver.PhantomJS(executable_path=r'/Users/zz358840/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')  
# 把所有章節爬完(建議手動先看一下有幾個章節)
while ch<12:
    #每個章節都從第1頁開始爬
    page=1
    # 合併真正所在地網址位置
    newurl=url+str(ch)+'-'+str(page)
    # http get requests
    driver.get(newurl)
    # 取出原始碼
    pageSource = driver.page_source
    # 格式化原始碼  
    soup=BeautifulSoup(pageSource,'html.parser')
    # 取出ID為pagenum的元素
    for pagenum in soup.select('#pagenum'): 
        src=pagenum
        print(src)
    srcstr=str(src)
    # 找到/位置(第1/33頁)
    index=srcstr.find("/")
    # 真正的總頁數位置 
    pagenum=int((srcstr[index+1:index+3])) 
    print ("ch check ok. ch"+str(ch)+" have "+str(pagenum)+" page")
    # 目前頁數小於總頁數就一直爬
    while page<=pagenum:
        newurl=url+str(ch)+'-'+str(page)
        driver.get(newurl)
        pageSource = driver.page_source
        soup=BeautifulSoup(pageSource,'html.parser')
        # 找到漫畫所在位置
        for img in soup.select('#TheImg'): 
            src=img['src'] 
            print(src)
        # http get requests
        r = requests.get("http:"+src)
        # 資料夾名稱 由章節為名稱
        dir_name=str(ch) 
        # 如果目錄不存在就建立目錄 不需要事先建立
        if not os.path.exists(dir_name): 
            os.makedirs(dir_name)
        # 儲存圖片(2進位格式)
        f=open(dir_name+'/'+str(ch)+'-'+str(page)+'.jpg','wb')
        f.write(r.content) 
        f.close
        print("ch:"+str(ch)+"-"+str(page)+" download ok")
        print()
        # 頁數+1
        page+=1
    # 章節+1
    ch+=1
# 全部爬完就結束
driver.close()  