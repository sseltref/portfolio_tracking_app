import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from kivy.uix.image import Image

class Button(Button):
    pass

class Main(TabbedPanel):
    pass


class MyApp(App):
    img_src = 'foo.png'

    def stock_data(self, ticker, period, interval, observation):
        ticker = yf.Ticker(ticker)
        ticker_history = ticker.history(period, interval)

        sf = ticker_history[observation]
        df = pd.DataFrame({'Date': sf.index, 'Values': sf.values})

        x = df['Date'].tolist()
        y = df['Values'].tolist()

        plt.style.use('dark_background')
        plt.plot(x, y)
        plt.ylabel('Price($)')
        plt.xlabel('Date', rotation=0)
        plt.savefig('foo.png')

    def build(self):
        #box = BoxLayout()
        #box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #return box
        return  Main()
if __name__ == '__main__':
    MyApp().run()

