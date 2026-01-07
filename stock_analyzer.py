import os
import requests
import pandas as pd

# Load API keys from environment variables
API_KEY = os.getenv("POLYGON_API_KEY")
API_KEY_ALPHA = os.getenv("ALPHA_VANTAGE_API_KEY")

if not API_KEY or not API_KEY_ALPHA:
    raise ValueError("Missing API keys. Set environment variables first.")


def fetch_values(url, path):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    for key in path:
        data = data[key]

    return pd.DataFrame(data)


def daily_averages(tick):
    url = f"https://api.massive.com/v2/aggs/ticker/{tick}/prev?adjusted=true&apiKey={API_KEY}"
    df = fetch_values(url, ["results"])

    df = df.astype({"c": float, "h": float, "l": float})
    latest = df.iloc[0]

    return {
        "closing": round(latest["c"], 2),
        "high": round(latest["h"], 2),
        "low": round(latest["l"], 2),
    }


def sma(tick, window):
    url = (
        f"https://api.massive.com/v1/indicators/sma/{tick}"
        f"?adjusted=true&window={window}&series_type=close&order=desc&limit=10"
        f"&apiKey={API_KEY}"
    )
    df = fetch_values(url, ["results", "values"])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["value"] = df["value"].astype(float)

    return round(df.iloc[0]["value"], 2)


def rsi(tick):
    url = (
        f"https://api.massive.com/v1/indicators/rsi/{tick}"
        f"?timespan=day&adjusted=true&window=14&order=desc&limit=10"
        f"&apiKey={API_KEY}"
    )
    df = fetch_values(url, ["results", "values"])

    df["value"] = df["value"].astype(float)
    return round(df.iloc[0]["value"], 2)


def macd(tick):
    url = (
        f"https://api.massive.com/v1/indicators/macd/{tick}"
        f"?timespan=day&adjusted=true&short_window=12&long_window=26"
        f"&signal_window=9&series_type=close&order=desc&limit=1"
        f"&apiKey={API_KEY}"
    )

    df = fetch_values(url, ["results", "values"])
    latest = df.iloc[0]

    return {
        "macd": round(float(latest["value"]), 2),
        "signal": round(float(latest["signal"]), 2),
        "histogram": round(float(latest["histogram"]), 2)
    }


def score_stock(data):
    score = 0.0
    max_score = 6.0

    diff_pct = (data["closing"] - data["sma_50"]) / data["sma_50"]
    score += max(min(diff_pct, 0.05), -0.05) * 20

    score += 0.75 if data["sma_50"] > data["sma_200"] else -0.75
    score += (data["rsi"] - 50) / 25

    macd_diff = data["macd"] - data["signal"]
    score += max(min(macd_diff / 5, 1), -1)

    score += max(min(data["histogram"] / 3, 1), -1)

    sentiment = data.get("sentiment", 0)
    score += max(min(sentiment * 2, 1), -1)

    return round(score, 2), max_score


def decision(score, max_score):
    confidence = round(score / max_score, 2)

    if confidence >= 0.7:
        return "STRONG BUY", confidence
    elif confidence >= 0.4:
        return "BUY", confidence
    elif confidence <= -0.7:
        return "STRONG SELL", confidence
    elif confidence <= -0.4:
        return "SELL", confidence
    else:
        return "HOLD", confidence


def fetch_news(ticker, limit=10):
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=NEWS_SENTIMENT&tickers={ticker}&limit={limit}"
        f"&apikey={API_KEY_ALPHA}"
    )
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    feed = data.get("feed", [])
    return [
        {
            "title": article.get("title", "No title"),
            "url": article.get("url", "#"),
            "source": article.get("source", "Unknown"),
            "sentiment": round(article.get("overall_sentiment_score", 0), 3)
        }
        for article in feed[:limit]
    ]


def news_sentiment(tick, limit=10):
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=NEWS_SENTIMENT&tickers={tick}&limit={limit}"
        f"&apikey={API_KEY_ALPHA}"
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    scores = [
        float(article["overall_sentiment_score"])
        for article in data.get("feed", [])
        if "overall_sentiment_score" in article
    ]

    return round(sum(scores) / len(scores), 3) if scores else 0.0


def analyze_stock(tick):
    tick = tick.upper()

    data = daily_averages(tick)
    data["sma_50"] = sma(tick, 50)
    data["sma_200"] = sma(tick, 200)
    data["rsi"] = rsi(tick)
    data |= macd(tick)

    data["sentiment"] = news_sentiment(tick)
    news_items = fetch_news(tick)

    score, max_score = score_stock(data)
    action, confidence = decision(score, max_score)

    return {
        "ticker": tick,
        "decision": action,
        "score": score,
        "confidence": confidence,
        "metrics": data,
        "news": news_items
    }
