import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def get_info(ticker):
    ticker = yf.Ticker(ticker)
    print(ticker.info)



def stock_data(ticker, period, interval, observation):
    ticker = yf.Ticker(ticker)
    ticker_history = ticker.history(period, interval)
    print(ticker.info)

    sf = ticker_history[observation]
    df = pd.DataFrame({'Date':sf.index, 'Values':sf.values})

    x = df['Date'].tolist()
    y = df['Values'].tolist()

    plt.style.use('dark_background')
    plt.plot(x,y)
    plt.ylabel('Price($)')
    plt.xlabel('Date', rotation=0)
    plt.show()

if __name__ == '__main__':
    #stock_data('TSLA', '1y', '1wk', 'Open')

    get_info("BTC")

'''
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):

    def build(self):
        box = BoxLayout()'''