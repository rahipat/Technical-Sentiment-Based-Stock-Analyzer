from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stock_logic import analyze_stock

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze/{ticker}")
def analyze(ticker: str):
    return analyze_stock(ticker.upper())
