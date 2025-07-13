import PySimpleGUI as sg
from pathlib import Path
from datetime import datetime

from config import BacktestConfig
from data import fetch_data, clean_data
from optimize import optimize_hilo, get_best
from strategy import compute_hilo
from report import plot_results, plot_comparison, save_to_excel
from pathlib import Path

# === determine the folder where this script lives ===
base_path = Path(__file__).resolve().parent

# === now create a Reports subfolder under that path ===
reports_dir = base_path / 'Reports'
reports_dir.mkdir(exist_ok=True)


# --- GUI Setup ---
sg.theme('DarkBlue14')  # Clean, modern theme
layout = [
    [sg.Text('📈 HiLo Strategy Backtester', font=('Helvetica', 18),
             justification='center', expand_x=True)],
    [sg.Frame(layout=[
        [sg.Text('Ticker Symbol:', size=(15, 1)), sg.Input(
            'SOL-AUD', key='-SYM-', size=(20, 1))],
        [sg.Text('Start Date:',    size=(15, 1)), sg.Input('', key='-START-', size=(20, 1)),
         sg.CalendarButton('Select', target='-START-', format='%Y-%m-%d')],
        [sg.Text('End Date:',      size=(15, 1)), sg.Input('', key='-END-',   size=(20, 1)),
         sg.CalendarButton('Select', target='-END-',   format='%Y-%m-%d')],
        [sg.Text('Transaction Cost:', size=(15, 1)),
         sg.Input('0.003', key='-COST-', size=(20, 1))],
        [sg.Text('Max HiLo Period:',  size=(15, 1)), sg.Slider(range=(
            5, 200), orientation='h', size=(25, 15), default_value=100, key='-MAX-')],
        [sg.Button('Run Backtest', font=('Helvetica', 12), size=(12, 1)),
         sg.Button('Quit', font=('Helvetica', 12), size=(8, 1))]
    ], title='Parameters', title_color='white', relief=sg.RELIEF_SUNKEN, tooltip='Adjust backtest settings')],
    [sg.StatusBar('', size=(60, 1), key='-STATUS-')]
]

window = sg.Window('HiLo Backtester', layout,
                   element_justification='center', finalize=True)

while True:
    event, vals = window.read()
    if event in (sg.WIN_CLOSED, 'Quit'):
        break
    if event == 'Run Backtest':
        sym = vals['-SYM-']
        start = vals['-START-']
        end = vals['-END-']
        cost = float(vals['-COST-'])
        maxp = int(vals['-MAX-'])

        window['-STATUS-'].update('🔄 Fetching data...')
        raw = fetch_data(sym, start, end)
        if raw.empty:
            sg.popup_error(f"No data for {sym} from {start} to {end}.")
            window['-STATUS-'].update('Ready')
            continue

        df = clean_data(raw)
        window['-STATUS-'].update('⚙️ Optimizing...')
        opt_df = optimize_hilo(df, range(10, maxp+1), cost)
        best, ret = get_best(opt_df)
        sg.popup(f"Optimal HiLo = {best} days (Return: {ret:.2f}x)")

        window['-STATUS-'].update('📊 Running final backtest...')
        final_df = compute_hilo(df, best, cost)
        final_df['HiLo Period'] = best

        window['-STATUS-'].update('📈 Generating plots & report...')
        reports_dir.mkdir(exist_ok=True)
        s0, s1 = df.index[0].strftime(
            '%Y-%m-%d'), df.index[-1].strftime('%Y-%m-%d')
        opt_png = reports_dir / f"{sym}_{s0}_{s1}_opt.png"
        cmp_png = reports_dir / f"{sym}_{s0}_{s1}_cmp.png"
        plot_results(opt_df, sym, out_file=opt_png)
        plot_comparison(final_df, best, sym, out_file=cmp_png)
        excel_file = reports_dir / f"{sym}_{s0}_{s1}_report.xlsx"
        save_to_excel(final_df, opt_df, [opt_png, cmp_png], excel_file)

        sg.popup('✅ Done', f"Report saved to:\n{excel_file}")
        window['-STATUS-'].update('Ready')

window.close()
