# data.py
import yfinance as yf
import pandas as pd


def fetch_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Download OHLCV data via updated yfinance API.
    """
    print(f"Fetching {symbol} from {start} to {end}...")
    df = yf.download(
        tickers=symbol,
        start=start,
        end=end,
        auto_adjust=False,
        group_by='column',
        progress=False
    )
    if df.empty:
        info = yf.Ticker(symbol).info
        if not info:
            print(f"No data for {symbol}.")
            return df
        print(f"Range empty; fetching full history for {symbol}.")
        df = yf.download(
            tickers=symbol,
            period="max",
            auto_adjust=False,
            group_by='column',
            progress=False
        )
    print(f"Data fetched: \n{df}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    if isinstance(cleaned.columns, pd.MultiIndex):
        cleaned.columns = cleaned.columns.droplevel(1)
    if 'Adj Close' not in cleaned.columns:
        raise KeyError("The 'Adj Close' column is missing from the data.")
    # Remove unnecessary columns if they exist
    for col in ["Volume", "Open", "Close"]:
        if col in cleaned.columns:
            del cleaned[col]
    # Remove timezone information
    cleaned.index = cleaned.index.tz_localize(None)
    return cleaned
