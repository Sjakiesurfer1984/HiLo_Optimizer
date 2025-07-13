from dataclasses import dataclass

@dataclass
class BacktestConfig:
    symbol: str                   # Ticker symbol, e.g. "SOL-AUD"
    start: str                    # Start date in 'YYYY-MM-DD' format
    end: str                      # End date in 'YYYY-MM-DD' format
    transaction_cost: float = 0.003  # Cost per trade (e.g. 0.003 = 0.3%)
