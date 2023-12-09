import time
import re
import json
import csv
import random
from selenium import webdriver
from lxml import etree
import lxml
from selenium.webdriver import ChromeOptions
import re
def Readsvgid(svg):#读取ID
    with open(svg,"r",encoding='utf-8') as f:
        text=f.read()
    textYX=re.findall('y="(.*?)"',text)
    return textYX
        

def Readsvg(svg):#读取文字
    with open(svg,"r",encoding='utf-8') as f:
        text=f.read()
    text=re.findall('.*?</text>',text)
    listall=[]
    for li in text:
        textl=re.findall('>(.*?)</text>',li)#获取文字
        for lk in textl:
            tel=re.findall('(.)',lk)
            listall.append(tel)
    return listall
def jiemi(css,id,svgtext):
     with open(css,"r",encoding='utf-8') as f:
         text=f.read()
     dict1={}
     dict2={}
     text1=re.findall('.(.*?) {',text)
     text2=re.findall('background: (.*?)px (.*?)px;',text)
     for i in range(len(text2)):
         dict1[text1[i]]=list(text2[i])     
     for key, value in dict1.items():
         y=-eval(value[1])
         k1=(-eval(value[0]))/14+1
         for j in range(len(id)):
             if eval(id[j])>=y:
                 v1=j+1
                 break
             dict1[key]=[int(k1),v1]
     for key, value in dict1.items():
         x=value[0]
         y=value[1]
         #if key.startswith('wdl'):
     dict2[key]=svgtext[y-1][x-1]
     return dict2
def jie(st,lis):
    si=st.replace("\n","").replace("/","").replace("<","").replace(">","").replace("svgmtsi","").replace("class=","").replace('div "review-words Hide"',"").replace("div","").replace('"less-words"',"").replace('a href="javascript:;"',"")
    si=si.replace('data-click-title="文字"',"").replace('data-click-title=文字',"")           
    sj=re.findall('"(wdl.*?)"',si)
    for ss in sj:
        s=lis[ss]
        si=si.replace(ss,s)
    si=si.replace('"',"").replace(" ","")
    si=re.sub('unfolddata.*',"",si)
    si=re.sub('imgsrc=https:.*pngalt=',"",si)
    si=re.sub('imgemoji-',"",si)
    si=re.sub("review-words","",si)
    return si     
    
svg="E:\\大学课程作业\\项目\\python\\美团\\jiemi.txt"
css="E:\\大学课程作业\\项目\\python\\美团\\duizhao.txt"
lia=Readsvgid(svg)
lib=Readsvg(svg)
lis=jiemi(css,lia,lib)
option=ChromeOptions()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
option.add_argument(f'user-agent={UA}')
option.add_experimental_option('useAutomationExtension', False)

#chrome_opt = webdriver.ChromeOptions()
#prefs = {"profile.managed_default_content_settings.images": 2}
#chrome_opt.add_experimental_option("prefs", prefs)
#Optionss=ChromeOptions()
#option.add_argument("--proxy-server=https://127.0.0.1:8080")
option.add_experimental_option('excludeSwitches',['enable-automation'])
web=webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe',options=option)#chrome_options=chrome_opt,,options=option
web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
web.implicitly_wait(15)
web.get("https://account.dianping.com/login?redir=https://www.dianping.com")
time.sleep(20)
with open("E:\\大学课程作业\\项目\\python\\美团\\sj.csv","r",encoding="utf-8") as f:
	reader=csv.reader(f)
	result=list(reader)
error=0
for lin in result:
    error=error+1
    if error<9:
        continue
    keyid=1
    link=lin[1]+"/review_all/p1?queryType=sortType&&queryVal=latest"
    nextue=lin[1]
    web.get(link)
    for handle in web.window_handles:      #转页面
        web.switch_to.window(handle)
        if '验证中心'  in web.title:
                time.sleep(130)
                web.get(link)
        if lin[0]  in web.title:
            mainWindown=web.current_window_handle
            break
    for handle in web.window_handles:      #转页面2
         web.switch_to.window(handle)
         if '验证中心' in web.title:
                time.sleep(130)
                web.get(link)
         if lin[0]  in web.title:
            mainWindown=web.current_window_handle
            break
    shop=[]
    name=lin[0]
    mask=web.find_elements_by_xpath('//*[@id="review-list"]/div[2]/div[1]/div[2]/div/div[2]')[0].text#评分
    number=web.find_elements_by_xpath('//span[@class="reviews"]')[0].text#人数
    num=web.find_elements_by_xpath('//div[@class="rank-info"]//span[@class="score"]/span')
    print(name)
    ll=[]
    for nu in num:
        ll.append(nu.text)
    shop.append(name)
    shop.append(mask)
    shop.append(number)
    shop.append(ll)
    with open("E:\\大学课程作业\\项目\\python\\美团\\sjpl.csv",'a+',newline="",encoding='utf-8') as f:
        writer= csv.writer(f)
        writer.writerow(shop)
    for i in range(1,25):#翻页解析评论
        webb=web.page_source
        webb=etree.HTML(webb)
        sps=webb.xpath('//div[@class="reviews-items"]/ul/li')#获取评论
        liss=[] 
        for text in sps:    
            lists=[]
            times=text.xpath('.//span[@class="time"]/text()')[0].replace(' ','').replace('\n','')
            if times.startswith('2021-08-0') is False:
                keyid=0
                break
            nameid=text.xpath('.//div[@class="dper-info"]/a/text()')[0].replace(' ','').replace('\n','')
            lists.append(nameid)
            lists.append(times)
            mas=text.xpath('.//div[@class="review-rank"]/span/@class')
            mas=eval(re.findall("sml-rank-stars sml-str(.*?) star",mas[0])[0])/10.0
            lists.append(mas)
            #zann=text.find_element_by_xpath('.//span[@class="actions"]/em')
            #zan=text.find_element_by_xpath('.//em')
            #if len(zan)!=0:
                #zan=zan[0].text
                #lists.append(zan)
            #else:
                #lists.append("0")
            comments2=text.xpath('.//div[@class="review-words Hide"]')#/text()|./div[@class="review-words Hide"]/svgmtsi/@class')
            if len(comments2)==0:
                 comments2=text.xpath('.//div[@class="review-words"]')
                #替换 直接改成解密
            comments2=etree.tostring(comments2[0],encoding="utf-8",method="html").decode()
            comments2=jie(comments2,lis)
            lists.append(comments2)
            liss.append(lists)
            print(nameid,"  ",times,mas)
        with open("E:\\大学课程作业\\项目\\python\\美团\\sjpl.csv",'a+',newline="",encoding='utf-8') as f:
            writer= csv.writer(f)
            for kk in liss:
                writer.writerow(kk)
        time.sleep(round(random.uniform(4,5),2))
        if keyid==0:
            break
        ur=nextue+"/review_all/p"+str(i+1)+"?queryType=sortType&&queryVal=latest"
        web.get(ur)
        for handle in web.window_handles:      #转页面
            web.switch_to.window(handle)
            if '验证中心'  in web.title:
                time.sleep(130)
            if "第"+str(i+1) in web.title:
                mainWindown=web.current_window_handle
                break
        for handle in web.window_handles:      #转页面2
            web.switch_to.window(handle)
            if '验证中心' in web.title:
                time.sleep(130)
            if "第"+str(i+1)  in web.title:
                mainWindown=web.current_window_handle
                break
        

