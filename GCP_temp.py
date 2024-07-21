from google.cloud import language_v1
import os
# 指定你要開啟的 txt 檔案的路徑
txt_file_path = "/Users/huangweiting/coding/CONSTRUCTION-CONTRACTS-AND-LEGAL-JUDGEMENTS/dataset/高雄高等行政法院 105 年度訴字第 288 號判決.txt"

# 開啟並讀取 txt 檔案
with open(txt_file_path, 'r', encoding='utf-8') as file:
    text = file.read()
def sample_analyze_entity_sentiment(gcs_content_uri):
    """
    Analyzing Entity Sentiment in text file stored in Cloud Storage

    Args:
      gcs_content_uri Google Cloud Storage URI where the file content is located.
      e.g. gs://[Your Bucket]/[Path to File]
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='judge-424401-cc7e37c36ce6.json'
    client = language_v1.LanguageServiceClient()

    # gcs_content_uri = 'gs://cloud-samples-data/language/entity-sentiment.txt'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {
        "gcs_content_uri": gcs_content_uri,
        "type_": type_,
        "language": language,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(f"Representative name for the entity: {entity.name}")
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(f"Entity type: {language_v1.Entity.Type(entity.type_).name}")
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(f"Salience score: {entity.salience}")
        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(f"Entity sentiment score: {sentiment.score}")
        print(f"Entity sentiment magnitude: {sentiment.magnitude}")
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(f"{metadata_name} = {metadata_value}")

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(f"Mention text: {mention.text.content}")
            # Get the mention type, e.g. PROPER for proper noun
            print(
                "Mention type: {}".format(
                    language_v1.EntityMention.Type(mention.type_).name
                )
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(f"Language of the text: {response.language}")

sample_analyze_entity_sentiment(text)