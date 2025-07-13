# strategy.py
import numpy as np
import pandas as pd


def compute_hilo(df: pd.DataFrame, period: int, transaction_cost: float) -> pd.DataFrame:
    """
    Apply HiLo strategy: rolling average high/low, generate signals, calculate returns.
    """
    # Make a copy so original df isn't modified
    df = df.copy()

    # Calculate rolling average of the High prices over 'period' days
    df['Avg Hi'] = df['High'].rolling(window=period).mean()
    # Calculate rolling average of the Low prices over 'period' days
    df['Avg Lo'] = df['Low'].rolling(window=period).mean()

    # Initialize the 'Signal' column with NaN
    df['Signal'] = np.nan
    # A 'buy' signal when today's close > yesterday's Avg Hi
    buy = df['Adj Close'] > df['Avg Hi'].shift(1)
    # A 'sell' signal when today's close < yesterday's Avg Lo
    sell = df['Adj Close'] < df['Avg Lo'].shift(1)

    # Assign 1 for buy signals, -1 for sell signals
    # This creates a new column 'Signal' with 1 for buy, -1 for sell, and NaN otherwise
    df.loc[buy, 'Signal'] = 1
    df.loc[sell, 'Signal'] = -1

    # Carry forward the last non-NaN signal to represent current position
    # .ffill() fills forward, .fillna(0) ensures any NaN (which always includes the first row) is set to 0
    df['Position'] = df['Signal'].ffill().fillna(0)

    # 1) magnitude of position change (0,1,2, etc.)
    trade_qty = df['Position'].diff().abs().fillna(0)

    # 2) notional value = trade_qty × price
    trade_value = trade_qty * df['Adj Close']

    # 3) cost = percentage fee × notional
    df['Cost'] = trade_value * transaction_cost
    # 4) express cost as a fraction of position value (≈ transaction_cost when trading 1 unit)
    df['Cost Pct'] = df['Cost'] / df['Adj Close']

    # Compute daily simple returns on 'Adj Close'
    df['Daily Return'] = df['Adj Close'].pct_change()

    # For each day, compute strategy multiplier:
    #   If position was LONG (1) yesterday: multiply by (1 + daily return)
    #   If position was SHORT (-1): multiply by 1/(1 + daily return)
    #   If FLAT (0): multiplier of 1 (no change)
    df['Strategy Return'] = np.where(
        df['Position'].shift(1) == 1,
        1 + df['Daily Return'],
        np.where(
            df['Position'].shift(1) == -1,
            1 / (1 + df['Daily Return']),
            1
        )
    )

    # Cumulative product of daily strategy returns gives overall growth
    df['Cumulative Return'] = df['Strategy Return'].cumprod()

    # ————————————————————————————————————————————————————

    # 5) subtract that fee from your raw strategy multiplier each day
    df['Net Strategy Return'] = df['Strategy Return'] - df['Cost Pct']

    # 6) build a second cumulative curve that includes the drag of fees
    df['Cumulative Return (net)'] = df['Net Strategy Return'].cumprod()

    # ————————————————————————————————————————————————————
    # after compute_hilo(df, best, cost) → yields final_df
    total_trades = df['Position'].diff().abs().sum()
    total_fees = df['Cost'].sum()
    print(df['Cost'])
    print(f"Total trades(unit changes): {total_trades: .0f}")
    # assuming price in AUD
    print(f"Total fees paid: {total_fees: .2f} AUD ")

    # Return the enriched DataFrame
    return df
