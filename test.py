import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from scipy.stats import pearsonr

# 讀取數據
data = pd.read_csv('judgements.csv')

# 數據預處理
data['text'] = data['text'].str.lower().str.replace('[^\w\s]', '').str.replace('\d+', '')

# 特徵提取
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['text'])

# 主題模型
lda = LatentDirichletAllocation(n_components=10, random_state=0)
lda.fit(X)

# 相關性分析
topics = lda.transform(X)
correlation, _ = pearsonr(topics, data['judgement'])