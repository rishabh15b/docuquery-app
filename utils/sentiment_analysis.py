from textblob import TextBlob

def analyze_sentiment(file_paths):
    sentiments = []
    for path in file_paths:
        try:
            with open(path, "r") as f:
                text_content = f.read()
                blob = TextBlob(text_content)
                sentiments.append({
                    "polarity": blob.sentiment.polarity,
                    "subjectivity": blob.sentiment.subjectivity,
                })
        except Exception as e:
            print(f"Error processing file {path}: {e}")
    return sentiments
