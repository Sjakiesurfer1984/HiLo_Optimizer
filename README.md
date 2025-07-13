A command line app that pulls historical financial data from Yahoo Finance (free), and calculates roling averages (adjustable windows) of the High and Low prices  of an assett. 

If today's stock/ETF/Crypto price is higher than avg_hi => BUY. If today's price is lower then avg_lo => Selll. 

The app simulates (backtests) trades and plots results. 


To run:

pip install - r requirements.txt

Then run main.py.

Alternatively, you can run the ap_gui.py. However, the PySimpleGUI package requires you to registrate. After a free trial period, you are then asked to pay. 

Or Pull the repository and run locally in your IDE of choice. 
