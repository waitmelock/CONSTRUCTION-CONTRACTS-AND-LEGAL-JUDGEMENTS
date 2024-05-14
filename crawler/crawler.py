import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

 
domain_url = 'https://opendata.judicial.gov.tw/dataset?categoryTheme4Sys%5B0%5D=051&sort.publishedDate.order=desc&page=1'
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(f'{domain_url}/api/FilesetLists/47180/file')	
button = browser.find_element_by_class_name('badge.badge-RAR-brd-r')
button.click()
 
soup = BeautifulSoup(browser.page_source, 'lxml')
trs = soup.find('table', {'class': 'grid links'}).find('tbody').find_all('tr')  #爬取表格所有列
 
for tr in trs:
    filename = tr.find('td').getText().strip().replace('/', '_')  #爬取表格的「資料範圍」欄位當做檔案名稱
    link = tr.find('a').get('href')  #爬取下載檔案連結
    response = requests.get(domain_url + link)