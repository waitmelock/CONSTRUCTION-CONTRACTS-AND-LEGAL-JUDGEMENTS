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
import pandas as pd
import itertools

# 關鍵字

key_input=['判決']
key_main2=['工程契約']#工程','契約'
key_sit=["天氣","颱風", "風災", "地震", "豪雨", "陰雨", "淹水", "水災", "洪水", "地質", "地貌", "地形", "地下水位", "疫情", "戰爭"]#"颱災"
key_main=["民法第227條"]
all_combinations = [key_input + list(combination) for combination in itertools.product(key_sit, key_main,key_main2)]

#訪問網站開頭
browser_urls = 'https://judgment.judicial.gov.tw/FJUD/default.aspx'
#解決反sel問題
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
browser = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
    "source":"""
            Object.defineProperty(navigator,'webdriver',{
                get: () => undefined
            })
            """
})
wait=WebDriverWait(browser,100,0.2)#等待時間限制和頻率

list_name="test.cvs"#"資料清單.csv"
floder="data_test"
dir_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/"+floder
# 檢查資料夾是否已存在，如果不存在，則創建新的資料夾

if not os.path.exists(dir_path):
    os.mkdir(dir_path)
    
if os.path.exists(dir_path+"/"+list_name):
    # 如果檔案存在，讀取 csv 檔案
    with open(dir_path+"/"+list_name, 'r',encoding='utf-8-sig') as csvFile:
        reader = csv.reader(csvFile)
        index_list = [row[0] for row in reader]
else:
    # 如果檔案不存在，創建一個新的 csv 檔案並寫入標題
    with open(dir_path+"/"+list_name, 'w', newline='', encoding='utf-8-sig') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['案例', 'URL', '關鍵字', '標籤'])
          
with open(dir_path+"/"+list_name, 'w', newline ='',encoding='utf-8-sig') as csvFile:
    field = ['案例','URL','關鍵字','標籤']
    dicWriter = csv.DictWriter(csvFile, fieldnames = field) #建立Writer物件
    dicWriter.writeheader() #寫入標題
    # 關鍵字搜尋
    for j in range(len(all_combinations)):
        browser.get(browser_urls)	
        #print(browser_urls)
        combination=all_combinations[j]
        file_name= '|'.join(combination)
        print(file_name)
        # 搜尋
        input_element = browser.find_element(By.ID,'txtKW')
        if j != 0:
            browser.execute_script("arguments[0].value = '';", input_element)
        input_element.send_keys(combination[0])
        input_element.send_keys(Keys.RETURN)
        print("初步搜尋完成")
        for i in range(len(combination) - 1):
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav > li:nth-child(2) > a'))).click()
            input_element=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtAKW")))
            input_element.send_keys(combination[i+1])
            input_element.send_keys(Keys.RETURN)
            print(f'第{i+2}步搜尋完成')
        #list顯示成功
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "active")))
        total_number=int(browser.find_element(By.XPATH,'//*[@id="result-count"]/ul/li/a/span').text)
        print(f'共{total_number}則判決')
        if total_number==0:
            print('本次搜尋無匹配資料')
            continue
        #檔案存入csv

        browser.switch_to.frame(0)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#hlTitle'))).click()
        for i in range(total_number):
            if (i>=1):#range(len(hltitle_elements)):
                break
            #print(i,hltitle_elements[i].text)#判決名
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            number_string=browser.find_element(By.CSS_SELECTOR, '#plPager > span:nth-child(1)').text
            #print(number_string)
            match = re.search('共 (\d+) / (\d+) 筆',number_string)#總共數量 現在頁數 總共頁數 
            current_number = int(match.group(1))
            total_number = int(match.group(2))
            
            soup = BeautifulSoup(browser.page_source, 'lxml')
            trs = soup.find('table')
            case_name=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#jud > div:nth-child(1) > div.col-td'))).text
            #print(trs.text)#內文
            with open(dir_path+'/'+case_name+'.txt', 'w') as file:
                file.write(trs.text)
                
            df = pd.read_csv(dir_path+"/"+list_name) 
            index_list = df['案例'].tolist()
            if case_name in index_list:
                # 如果案號已存在，更新關鍵字欄位
                df.loc[df['案例'] == case_name, '關鍵字'] += ', ' + '|'.join(combination)
                df.loc[df['案例'] == case_name, '標籤'] += "|重複"
                # 將案號存入 txt 檔案
                with open('案號.txt', 'a') as file:
                    file.write(case_name + '\n')
                continue
                
            try:
                ele=wait.until(EC.presence_of_element_located((By.ID, "hlExportPDF")))
                href=ele.get_attribute('href')
                dicWriter.writerow({'案例':case_name,'URL':href,'關鍵字':combination[len(key_input)]})
                #print(case_name)
            except TimeoutException:
                dicWriter.writerow({'案例':case_name,'URL':href,'關鍵字':combination[len(key_input)],'標籤':"NOPDF"})
                continue

            #print(href)#pdf url
            print(f'{i+1}:{case_name}')
            time.sleep(5)
            if current_number==total_number:
                continue
            else:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hlNext"]'))).click()
csvFile.close #關閉檔案

print('檔案儲存成功')


