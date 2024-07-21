# Imports the Google Cloud client library
from google.cloud import language_v1
txt_file_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/dataset/高雄高等行政法院 105 年度訴字第 288 號判決.txt"

# Instantiates a client
client = language_v1.LanguageServiceClient()
with open(txt_file_path, 'r', encoding='utf-8') as file:
    text = file.read()
# The text to analyze
document = language_v1.types.Document(
    content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(
    request={"document": document}
).document_sentiment

print(f"Text: {text}")
print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")