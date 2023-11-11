from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf


class StockData(BaseModel):
    symbol: str = "Stock symbol"
    open: float = "Opening price"
    high: float = "Highest price during the day"
    low: float = "Lowest price during the day"
    close: float = "Closing price"


app = FastAPI()


@app.get("/{symbol}", response_model=StockData)
async def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")

    if not hist.empty:
        return StockData(
            symbol=symbol,
            open=hist['Open'][0],
            high=hist['High'][0],
            low=hist['Low'][0],
            close=hist['Close'][0]
        )
    else:
        return {"error": "No data found for the given symbol."}
