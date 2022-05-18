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
import sqlite3
from sqlite3 import Error

class Button(Button):
    pass

class Main(TabbedPanel):
    pass


class MyApp(App):
    img_src = 'foo.png'

    @staticmethod
    def create_connection(db):
        conn = None

        try:
            conn = sqlite3.connect(db)
        except Error as e:
            print(e)

        return conn

    def make_transaction(self, conn, tr_date, currency1, currency2, volume):
        cur = conn.cursor()
        cur.execute('INSERT INTO history(tr_date, currency1, currency2, volume) VALUES (?, ?, ?, ?)',
                    (tr_date, currency1, currency2, volume))
        conn.commit()

    ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''

    conn_tr = create_connection('Database/database.db')
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

