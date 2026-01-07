# Stock Analyzer Dashboard

A full-stack stock analysis application that evaluates U.S. equities using technical indicators and news sentiment to generate trading signals.

The project consists of a Python backend that aggregates and analyzes financial data, and a lightweight HTML/CSS/JavaScript frontend that presents results in an interactive dashboard.



## Features

* Technical analysis using:

  * 50-day and 200-day Simple Moving Averages (SMA)
  * Relative Strength Index (RSI)
  * MACD (Moving Average Convergence Divergence)

* Scoring and decision engine

  * Combines technical indicators and sentiment
  * Outputs: STRONG BUY, BUY, HOLD, SELL, STRONG SELL
  * Includes a confidence score

* News sentiment analysis

  * Aggregates recent financial news
  * Computes an overall sentiment score
  * Displays article-level sentiment

* Client-side portfolio tracking

  * Save analyzed stocks to a portfolio
  * Persisted using browser localStorage

* Interactive frontend

  * Asynchronous API calls
  * Input validation and loading states



## Tech Stack

### Backend

* Python
* FastAPI
* Pandas
* Requests
* Polygon.io API (market data)
* Alpha Vantage API (news sentiment)

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript (ES6)


## API Key Setup

This project uses environment variables to securely manage API keys.

### Required APIs

* Polygon.io
* Alpha Vantage

### Environment Variables

Mac/Linux:

```bash
export POLYGON_API_KEY="your_key_here"
export ALPHA_VANTAGE_API_KEY="your_key_here"
```

Windows (PowerShell):

```powershell
setx POLYGON_API_KEY "your_key_here"
setx ALPHA_VANTAGE_API_KEY "your_key_here"
```



## Running the Project

1. Install backend dependencies:

```bash
pip install -r requirements.txt
```

2. Start the backend server:

```bash
uvicorn stock_analyzer:app --reload
```

3. Open the frontend:
   Open `frontend/index.html` in a browser.



## Example Output

* Ticker: AAPL
* Decision: HOLD
* Confidence: 48%
* Indicators: RSI, MACD, SMA crossover
* Sentiment: Neutral



## Future Improvements

* More Historical backtesting
* Price and indicator charting
* User authentication and saved portfolios
* Cloud deployment
* Additional indicators (Bollinger Bands, VWAP)



## Author

Rahi Patel
Computer Science Student
