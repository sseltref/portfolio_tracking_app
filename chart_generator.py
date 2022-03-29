import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def stock_data(ticker, period, interval, observation):
    ticker = yf.Ticker(ticker)
    ticker_history = ticker.history(period, interval)

    sf = ticker_history[observation]
    df = pd.DataFrame({'Date':sf.index, 'Values':sf.values})

    x = df['Date'].tolist()
    y = df['Values'].tolist()

    plt.style.use('dark_background')
    plt.plot(x,y)
    plt.ylabel('Price($)')
    plt.xlabel('Date', rotation=0)
    plt.savefig('foo.png')


stock_data('TSLA', '1y', '1wk', 'Open')