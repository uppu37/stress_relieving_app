from transformers import pipeline

# Load pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

def detect_mood(text):
    result = sentiment_pipeline(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == "NEGATIVE":
        mood = "Stressed or Sad"
    else:
        mood = "Happy or Calm"
        
    return mood, score