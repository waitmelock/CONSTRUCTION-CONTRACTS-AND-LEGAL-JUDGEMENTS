from google.cloud import language_v1
from google.cloud.language import Entity
# from google.cloud.language import types
import os


# 指定你要開啟的 txt 檔案的路徑
txt_file_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/dataset/高雄高等行政法院 105 年度訴字第 288 號判決.txt"

# 開啟並讀取 txt 檔案
with open(txt_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 打印出 txt 檔案的內容
print(text)
text= '想與姊妹掏來個下午茶談天時光，應該不少人都會想到咖啡廳聚集地 - 捷運中山站，除了幾間著名大家耳熟能詳的咖啡'
def analyze_entities(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='judge-424401-cc7e37c36ce6.json'
    # 實例化一個客戶端
    client = language_v1.LanguageServiceClient()
    # 要分析的文本
    text = text
    document = language_v1.Document(
                                content=text,
                                type_=language_v1.Document.Type.PLAIN_TEXT)
    # 檢測文本的情緒
    entities = client.analyze_entities(document=document)(request={'document': document}).entities
    
    for entity in entities:
        print('=' * 20)
        print('     名稱: {}'.format(entity.name))
        print('     類型: {}'.format(language_v1.Entity.Type(entity.type_).name))
        print('     重要性: {}'.format(entity.salience))

analyze_entities(text)



