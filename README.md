A command line app that pulls historical financial data from Yahoo Finance (free), and calculates roling averages (adjustable windows) of the High and Low prices  of an assett. 

If today's stock/ETF/Crypto price is higher than avg_hi => BUY. If today's price is lower then avg_lo => Selll. 

The app simulates (backtests) trades and plots results. 


To run:

pip install - r requirements.txt

Then run main.py.

Alternatively, you can run the ap_gui.py. However, the PySimpleGUI package requires you to registrate. After a free trial period, you are then asked to pay. 

Or Pull the repository and run locally in your IDE of choice. 



Set your asset's ticker. This must be equal to the ticker symbols used on Yahoo Finance. https://au.finance.yahoo.com/

Bitcoin: BTC-USD, or BTC-AUD
Ethereum: ETH-AUD, or ETH-USD

ETF examples:
SPY
IVV

Stocks:
GOOG
META

Then set the time period for which you'd like to fetch historical Open, High, Low, Close, Volune data, all in the first line of the main() loop: 


def main():
    cfg = BacktestConfig(symbol='BTC-USD', start='2020-07-06',
                         end='2025-07-06', transaction_cost=0.003)  # transaction cost is a percentage, e.g. 0.003 equals 0.3% of the trade value.
Run the programme. It will produce an excel report with Data, Optimization and Plots tabs.

Data tab content:
<img width="1760" height="148" alt="image" src="https://github.com/user-attachments/assets/c09b0e69-5c1d-4df3-9994-77a252ef03b0" />

Optimization tab content:

<img width="748" height="648" alt="image" src="https://github.com/user-attachments/assets/f5958651-3de9-461f-b7a3-451f4abea0fa" />

Plots tab content:
<img width="1875" height="1094" alt="image" src="https://github.com/user-attachments/assets/5fff0b6d-cd50-4ab9-88e2-d35e7e254572" />

<img width="1875" height="1094" alt="image" src="https://github.com/user-attachments/assets/238758cb-3b60-4736-b3b5-4a11370e9134" />


<img width="1875" height="1094" alt="image" src="https://github.com/user-attachments/assets/36654b8f-657d-4a35-a771-2368941737a1" />


