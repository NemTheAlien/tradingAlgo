import yfinance as yf
import pandas as pd
from datetime import date
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import configurations as cfg

def get_sma(symbol, start_date, end_date, window):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    close_values = data['Close']

    # Calculate the Simple Moving Average (SMA)
    sma_values = close_values.rolling(window=window).mean()

    return sma_values

def getHistoricalData(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    close_values = data['Close']

    return close_values

def trading_algorithm(symbol, start_date, end_date, window):
    # Get the closing prices and SMA values
    close_values_sma = get_sma(symbol, start_date, end_date, window)
    close_values = getHistoricalData(symbol, start_date, end_date)

    # Initialize variables for tracking positions
    position = None  
    positions = []  # To store the positions for each day

    # Loop through each day and determine the position
    for i in range(len(close_values_sma)):
        if close_values_sma[i] > close_values[i]:
            if position != 'Buy':  
                position = 'Buy'
                positions.append(position)
            else:
                positions.append(None) 
        elif close_values_sma[i] < close_values[i]:
            if position != 'Sell': 
                position = 'Sell'
                positions.append(position)
            else:
                positions.append(None)
        else:
            positions.append(None) 

    return positions

def executeOrder(positions):
    #this function should take in the positions from the account currently
    #check if its in line with the positions calculated from the trading algorithim and execute buy or sell orders
    trading_client = TradingClient(cfg.API_KEY, cfg.SECRET_KEY, paper=True)
    market_buyOrder_data = MarketOrderRequest(
                    symbol="AAPL",
                    qty=25,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
    market_sellOrder_data = MarketOrderRequest(
                    symbol="AAPL",
                    qty=25,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
    i = len(positions)-1
    if positions[i] == "Buy":
        #buy order 
        market_order = trading_client.submit_order(
            order_data=market_buyOrder_data
           )
        print("Placed buy order for 25 AAPL shares")
    elif positions[i] == "Sell":
        #sell order
        market_order = trading_client.submit_order(
            order_data=market_sellOrder_data
            )
        print("Placed sell order for 25 AAPL shares")
    else:
        #do nothing
        print("No buy or sell order")

symbol = "AAPL" 
start_date = "2023-01-01"
end_date = date.today()
window = 15  

positions = trading_algorithm(symbol, start_date, end_date, window)
x = len(positions)-1
print(positions[x],positions[x-1],positions[x-2])
executeOrder(positions)
