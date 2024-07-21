import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
import os
import re
import csv


# 關鍵字
key_input=['建字','情事變更','判決']
file_name= '和'.join(key_input)
urls=[]
#serAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537"
options = webdriver.ChromeOptions()
prefs={
    'profile.default_content_settings.popups':0,
    'download.default_directory':os.getcwd()
}
options.add_experimental_option('prefs',prefs)
ua = UserAgent()
userAgent = ua.random
while ('Mobile' or 'Android' or 'iphone') in userAgent:
    userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
browser_urls = 'https://judgment.judicial.gov.tw/FJUD/default.aspx'
browser = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
    "source":"""
            Object.defineProperty(navigator,'webdriver',{
                get: () => undefined
            })
            """
})
wait=WebDriverWait(browser,50,0.2)
browser.get(browser_urls)	
 # 找到輸入欄位並輸入資料
input_element = browser.find_element(By.ID,'txtKW')
input_element.send_keys(key_input[0])
input_element.send_keys(Keys.RETURN)
print("input complete")
print("submit complete")
i=len(key_input)
for i in range(len(key_input) - 1):
   wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav > li:nth-child(2) > a'))).click()
   input_element=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtAKW")))
   input_element.send_keys(key_input[i+1])
   input_element.send_keys(Keys.RETURN)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
#time.sleep(5)
browser.switch_to.frame(0)
number_string=browser.find_element(By.CSS_SELECTOR, 'div#plPager').find_element(By.TAG_NAME,"span").text

print(number_string)
match = re.search('共 (\d+) 筆 . 現在第 (\d+) / (\d+) 頁',number_string)
total_number = int(match.group(1))
current_pages = int(match.group(2))
total_pages = int(match.group(3))
#print(total_number,current_pages,total_pages)

    
#hltitle_elements = browser.find_elements(By.XPATH,'//table[@id="jud" and @class="jub-table"]//a[@class="hlTitle_scroll"]')
with open(file_name+'資料清單.csv', 'w', newline ='',encoding='utf-8-sig') as csvFile: #開啟檔案
    field = ['案例','URL']
    dicWriter = csv.DictWriter(csvFile, fieldnames = field) #建立Writer物件
    dicWriter.writeheader() #寫入標題
    for current_pages in range(0,25):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#jud.jub-table a.hlTitle_scroll')))
        hltitle_elements = browser.find_elements(By.CSS_SELECTOR, 'table#jud.jub-table a.hlTitle_scroll')
        # 在這裡放入你想要重複的操作
        for i in range(len(hltitle_elements)):
            print(i)
            #print(i,hltitle_elements[i].text)#檔名
            case_name=hltitle_elements[i].text
            
            #element = browser.find_element(By.CSS_SELECTOR, 'table#jud.jub-table a.hlTitle_scroll')
            browser.execute_script("arguments[0].click();",  hltitle_elements[i])
            
            # hltitle_elements[i].click()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            soup = BeautifulSoup(browser.page_source, 'lxml')
            trs = soup.find('table')
            #print(trs.text)#內文
            try:
                ele=wait.until(EC.presence_of_element_located((By.ID, "hlExportPDF")))
                href=ele.get_attribute('href')
                urls.append(href)
                dicWriter.writerow({'案例':case_name,'URL':href})
                print(case_name)
            except TimeoutException:
                browser.back()
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
                browser.switch_to.frame(0)
                #hltitle_elements = browser.find_elements(By.XPATH,'//table[@id="jud" and @class="jub-table"]//a[@class="hlTitle_scroll"]')
                hltitle_elements = browser.find_elements(By.CSS_SELECTOR, 'table#jud.jub-table a.hlTitle_scroll')
                continue
            #print(href)#pdf url
            browser.back()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
            browser.switch_to.frame(0)
            #hltitle_elements = browser.find_elements(By.XPATH,'//table[@id="jud" and @class="jub-table"]//a[@class="hlTitle_scroll"]')
            hltitle_elements = browser.find_elements(By.CSS_SELECTOR, 'table#jud.jub-table a.hlTitle_scroll')
        element_wait=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list-pager:nth-child(5) > #plPager #hlNext')))
        element_wait.click()
        print('sussese')
        time.sleep(5)
csvFile.close #關閉檔案
