# main.py
from pathlib import Path
from config import BacktestConfig
from data import fetch_data, clean_data
from optimize import optimize_hilo, get_best
from strategy import compute_hilo
from report import plot_results, plot_comparison, save_to_excel, plot_signals_with_returns


def main():
    cfg = BacktestConfig(symbol='CRV-USD', start='2020-07-06',
                         end='2025-07-06', transaction_cost=0.003)
    raw = fetch_data(cfg.symbol, cfg.start, cfg.end)
    if raw.empty:
        print("No data fetched; exiting.")
        return
    clean_df = clean_data(raw)
    # build filename using dates from df.index
    start_date = clean_df.index[0].strftime('%Y-%m-%d')
    end_date = clean_df.index[-1].strftime('%Y-%m-%d')

    opt = optimize_hilo(clean_df, range(10, 101), cfg.transaction_cost)
    best, ret = get_best(opt)
    print(f"Optimal HiLo: {best} days → Return: {ret:.2f}x")
    final = compute_hilo(clean_df, best, cfg.transaction_cost)
    # Add HiLo period metadata column
    final['HiLo Period'] = best

    reports_dir = Path(__file__).parent / 'Reports'
    reports_dir.mkdir(exist_ok=True)

    # 1) ensure Reports folder lives next to your script
    R = Path(__file__).resolve().parent / 'Reports'
    R.mkdir(exist_ok=True)

    # 2) build three filenames
    p1 = R / f"{cfg.symbol}_{start_date}_{end_date}_opt.png"
    p2 = R / f"{cfg.symbol}_{start_date}_{end_date}_cmp.png"
    p3 = R / f"{cfg.symbol}_{start_date}_{end_date}_signals.png"

    # 3) save each chart
    plot_results(opt,   cfg.symbol, out_file=p1)
    plot_comparison(final, best,     cfg.symbol, out_file=p2)
    plot_signals_with_returns(final, best, cfg.symbol, out_file=p3)

    # 4) write your Excel and embed all three
    excel_file = R / f"{cfg.symbol}_{start_date}_{end_date}_report.xlsx"
    save_to_excel(
        df=final,
        opt_df=opt,
        imgs=[p1, p2, p3],
        out_path=excel_file
    )

    print(f"Report generated: {excel_file}")

    # delete the temporary plot files
    for img in [p1, p2, p3]:
        try:
            img.unlink()
        except OSError:
            pass


if __name__ == '__main__':
    main()
