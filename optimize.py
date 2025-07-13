# optimize.py
import pandas as pd
from strategy import compute_hilo


def optimize_hilo(df: pd.DataFrame, periods: range, transaction_cost: float) -> pd.DataFrame:
    """
    Test a range of HiLo periods and return a DataFrame of final 
    gross and net cumulative returns.
    """
    records = []
    for p in periods:
        res = compute_hilo(df, p, transaction_cost)
        gross_end = res['Cumulative Return'].iloc[-1]
        net_end = res['Cumulative Return (net)'].iloc[-1]
        records.append({
            'HiLo': p,
            'Cumulative Return %': gross_end,
            'Cumulative Return (net) %': net_end
        })
    return pd.DataFrame(records)


def get_best(results: pd.DataFrame) -> tuple[int, float]:
    """
    Return the HiLo period with the highest cumulative return and its return.
    """
    idx = results['Cumulative Return %'].idxmax()
    best_period = int(results.loc[idx, 'HiLo'])
    best_return = float(results.loc[idx, 'Cumulative Return %'])
    return best_period, best_return
