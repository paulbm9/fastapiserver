from fastapi import FastAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

app = FastAPI()
app.title = "SentimentAI API"
app.version = "0.9.21"
app.description = "Api Rest SentimentAI realizado con Python"

@app.get("/get_tweets", tags=["Social Api"])
async def get_tweets(text: str):
    return [
    {
        "User": "AndreaCordova",
        "Date_created": "2023-07-01 12:30:45",
        "Number_of_likes": 12,
        "Source_of_tweet": "Twitter Web App",
        "Tweet": "¡El chocolate es mi felicidad! 🍫❤ #AmoElChocolate"
    },
    {
        "User": "Santiago_Lpz",
        "Date_created": "2023-07-01 12:45:20",
        "Number_of_likes": 0,
        "Source_of_tweet": "TweetDeck",
        "Tweet": "Disfrutando de un delicioso chocolate caliente en este día frío. ☕❄"
    },
    {
        "User": "CarlosPerez87",
        "Date_created": "2023-07-01 13:05:10",
        "Number_of_likes": 2,
        "Source_of_tweet": "Twitter for Android",
        "Tweet": "Nunca es demasiado chocolate. ¡Siempre es buen momento para disfrutarlo!"
    },
    {
        "User": "ChocolateEnMiVida",
        "Date_created": "2023-07-01 13:20:55",
        "Number_of_likes": 5,
        "Source_of_tweet": "Twitter iPhone",
        "Tweet": "Mis días son más dulces con un toque de chocolate. 🌈🍫"
    },
    {
        "User": "AnaRodriguez_",
        "Date_created": "2023-07-01 13:40:30",
        "Number_of_likes": 1,
        "Source_of_tweet": "Twitter Web App",
        "Tweet": "¡Hoy probé un nuevo postre de chocolate y estoy en el cielo! 😋✨"
    }
        ]
    


@app.get("/sentiment-analysis", tags=['Analyzer'])
async def analyze_sentiment():
    # Logica de interaccion con la API de la red social
    twitter_info = [
    {
        "User": "AndreaCordova",
        "Date_created": "2023-07-01 12:30:45",
        "Number_of_likes": 12,
        "Source_of_tweet": "Twitter Web App",
        "Tweet": "¡El chocolate es mi felicidad! 🍫❤ #AmoElChocolate"
    },
    {
        "User": "Santiago_Lpz",
        "Date_created": "2023-07-01 12:45:20",
        "Number_of_likes": 0,
        "Source_of_tweet": "Twitter iPhone",
        "Tweet": "Disfrutando de un delicioso chocolate caliente en este día frío. ☕❄"
    },
    {
        "User": "CarlosPerez87",
        "Date_created": "2023-07-01 13:05:10",
        "Number_of_likes": 2,
        "Source_of_tweet": "Twitter for Android",
        "Tweet": "Nunca es demasiado chocolate. ¡Siempre es buen momento para disfrutarlo!"
    },
    {
        "User": "ChocolateEnMiVida",
        "Date_created": "2023-07-01 13:20:55",
        "Number_of_likes": 5,
        "Source_of_tweet": "Twitter iPhone",
        "Tweet": "Mis días son más dulces con un toque de chocolate. 🌈🍫"
    },
    {
        "User": "AnaRodriguez_",
        "Date_created": "2023-07-01 13:40:30",
        "Number_of_likes": 1,
        "Source_of_tweet": "Twitter Web App",
        "Tweet": "¡Hoy probé un nuevo postre de chocolate y estoy en el cielo! 😋✨"
    }
    ]

    # Inicializar variables para estadísticas
    total_compound_score = 0.0
    total_positive_score = 0.0
    total_neutral_score = 0.0
    total_negative_score = 0.0
    total_likes = 0
    min_date = datetime.max
    max_date = datetime.min

    # Análisis de sentimiento para cada tweet
    analyzer = SentimentIntensityAnalyzer()

    for tweet in twitter_info:
        text = tweet["Tweet"]
        sentiment_scores = analyzer.polarity_scores(text)

        # Agregamos la información de sentimiento al diccionario del tweet
        tweet["Sentiment"] = {
            "Compound": sentiment_scores["compound"],
            "Positive": sentiment_scores["pos"],
            "Neutral": sentiment_scores["neu"],
            "Negative": sentiment_scores["neg"]
        }

        # Actualizamos las variables para estadísticas
        total_compound_score += sentiment_scores["compound"]
        total_positive_score += sentiment_scores["pos"]
        total_neutral_score += sentiment_scores["neu"]
        total_negative_score += sentiment_scores["neg"]
        total_likes += tweet["Number_of_likes"]

        # Actualizamos las fechas mínima y máxima
        tweet_date = datetime.strptime(tweet["Date_created"], "%Y-%m-%d %H:%M:%S")
        if tweet_date < min_date:
            min_date = tweet_date
        if tweet_date > max_date:
            max_date = tweet_date

    # Calcular los promedios y preparar resultados en formato JSON
    total_tweets = len(twitter_info)
    average_compound_score = total_compound_score / total_tweets if total_tweets > 0 else 0.0
    average_positive_score = total_positive_score / total_tweets if total_tweets > 0 else 0.0
    average_neutral_score = total_neutral_score / total_tweets if total_tweets > 0 else 0.0
    average_negative_score = total_negative_score / total_tweets if total_tweets > 0 else 0.0
    average_likes = total_likes / total_tweets if total_tweets > 0 else 0.0

    result = {
        "average_sentiment": {
            "compound": average_compound_score,
            "positive": average_positive_score,
            "neutral": average_neutral_score,
            "negative": average_negative_score
        },
        "average_likes_per_tweet": average_likes,
        "total_tweets": total_tweets,
        "min_tweet_date": min_date.strftime('%Y-%m-%d %H:%M:%S'),
        "max_tweet_date": max_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    return result
