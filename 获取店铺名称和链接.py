import time
import re
import json
import csv
import random
from selenium import webdriver
from lxml import etree
from selenium.webdriver import ChromeOptions
option=ChromeOptions()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
option.add_argument(f'user-agent={UA}')
option.add_experimental_option('useAutomationExtension', False)

#chrome_opt = webdriver.ChromeOptions()
#prefs = {"profile.managed_default_content_settings.images": 2}
#chrome_opt.add_experimental_option("prefs", prefs)
#Optionss=ChromeOptions()
#option.add_argument("--proxy-server=https://127.0.0.1:8080")
option.add_experimental_option('excludeSwitches',['enable-automation'])
web=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=option)#chrome_options=chrome_opt,,options=option
web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
web.implicitly_wait(15)
web.get("https://account.dianping.com/login?redir=https://www.dianping.com")
time.sleep(15)
urll="http://www.dianping.com/shanghai/ch10/p1"
web.get(urll)
for handle in web.window_handles:      #转页面内到休闲娱乐
        web.switch_to.window(handle)
        if '验证中心'  in web.title:
                time.sleep(130)
        if "生活"not in web.title:
            mainWindown=web.current_window_handle
            break
ls=web.find_elements_by_xpath('//div[@class="tit"]')
for ll in ls:
    lis=[]
    name=ll.find_elements_by_xpath('./a/h4')[0].text
    link=ll.find_elements_by_xpath('./a')[0].get_attribute("href")
    lis.append(name)
    lis.append(link)
    with open(r"C:\Users\徐嘉艺\Desktop\2021年暑期\name.csv",'a+',newline="",encoding='utf-8') as f:    #获取每家店铺的链接
            writer= csv.writer(f)
            writer.writerow(lis)
for i in range(2,5):
    time.sleep(round(random.uniform(4,5),2))
    urll="http://www.dianping.com/shanghai/ch10/p"+str(i)
    web.get(urll)
    for handle in web.window_handles:      #转页面内到休闲娱乐
        web.switch_to.window(handle)
        if '验证中心'  in web.title:
                time.sleep(130)
        if "第"+str(i) in web.title:
            mainWindown=web.current_window_handle
            break
    ls=web.find_elements_by_xpath('//div[@class="tit"]')
    for ll in ls:
        lis=[]
        name=ll.find_elements_by_xpath('./a/h4')[0].text
        link=ll.find_elements_by_xpath('./a')[0].get_attribute("href")
        lis.append(name)
        lis.append(link)
        print(lis)
        with open(r"C:\Users\徐嘉艺\Desktop\2021年暑期\name.csv",'a+',newline="",encoding='utf-8') as f:
            writer= csv.writer(f)
            writer.writerow(lis)
