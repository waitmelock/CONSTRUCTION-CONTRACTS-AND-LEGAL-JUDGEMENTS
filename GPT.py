import requests
import pdfplumber
import openai
import re
from glob import glob
from typing import Optional
import os

openai.api_key = "sk-proj-OuboBIhvWoOLgBy5hoVHT3BlbkFJPNmcd98QbQHUtzsgOYCh"

TLDRParameter = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 200,
    "temperature": 0.3,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "stop": ["\n\n"]
}

tldr_tag = "\n\n TL;DR:"
# current_path= "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/data/"
# new_folder_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/check227-2/"
# if not os.path.exists(new_folder_path):
#         print("error")

# if __name__ == '__main__': 
#     paths = glob(current_path+"高雄高等行政法院 105 年度訴字第 288 號判決.txt")#'*.txt')
#     print("處理檔案: ",paths)
#     dic = {}
#     for i, path in enumerate(paths):
#         with open(path, 'r', encoding='utf-8') as file:
#             text = file.read()
#         for index, page in enumerate(text):
#             content = page.extract_text() + tldr_tag
#             response = openai.ChatCompletion.create(prompt=content, **TLDRParameter
#                                                     )
#             print(f"Page {index + 1}:\n")
#             print(response["choices"][0]["text"])
#             print("\n\n")

current_path= "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/dataset/高雄高等行政法院 105 年度訴字第 288 號判決.txt"

paths = glob(current_path)
print("處理檔案: ",paths)
dic = {}

for i, path in enumerate(paths):
    if dic.get(path) == None:
        dic[path] = {'main_text':'', 'facts_and_reasons':''}
        # 建立空字典來儲存"主文"和"事實及理由"

    with open(path, 'r',encoding="utf-8") as file:
        text = file.read()
    # 讀取剛剛轉檔完成的評議書txt檔

    # text = re.sub('(','(', text)
    # text = re.sub(')',')', text)
    # text = re.sub(':',':', text)
    text = re.sub(' ','', text)
    text = re.sub('\n','!', text)
    # 將標點符號統一成全形

    pattern = re.compile(r'\s+(主*文)([\S\s]+?)(事實及理由|事實及理)([\S\s]+?)(中華民國[\S \d]+年[\S \d]+月[\S \d]+日[\s]*?)')
    match = pattern.search(text)
    # 擷取從"主文"到"日期"之間的內容
    if match is not None:
        dic[path]['main_text'] = match.group(2)
        dic[path]['facts_and_reasons'] = match.group(4)
    # 將"主文"和"事實及理由"個別儲存
    else:
            print(f"No match found in file {path}")
    pattern = re.compile(r'\s+(一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)+( )*(程序事項|申請人等之主張|申請人之主張|申請人主張|申請人等之主張|相對人之主張|相對人主張|相對人 A○○之主張|相對人\(A○○產物\)之主張|相對人 B○○之主張|相對人\(B○○\)之主張|相對人○○○銀行之主張|相對人○○○人壽之主張|相對人 A○○保經之主張|相對人○○○產物之主張|相對人 B○○人壽之主張|兩造不爭執之事實|兩造不爭執事實|兩造不爭執之事項|本件兩造爭執之要旨|本件爭點|判斷理由|綜上所述|綜上|據上論結)[:\s]*')
    tmp = pattern.split(dic[path]['facts_and_reasons'])
    # 將每個段落切割並存入字典, 以利後續擷取需要使用的段落

    dic[path]['facts_and_reasons'] = list(map(lambda x: re.sub('\s', '', x), [j for j in tmp if j != None and j != '']))
    print("評議書: ", path)
    print("主文內容: ", dic[path]['main_text'])
    print("\n")
    print("事實及理由內容: ", tmp)

print("*"*50)
print("資料整理完成")
# for index, page in enumerate(text):
content = text + tldr_tag
response = openai.ChatCompletion.create(prompt=content, **TLDRParameter
                                        )
print(f"Page:\n")
print(response["choices"][0]["content"])
print("\n\n")